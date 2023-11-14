//
//
//

#ifndef SLIDER_H
#define SLIDER_H

#include "def.h"
#include "epos4/epos4.h"
#include "util.h"
#include "ErrorDef.h"


class Slider {
public:
    enum class Command {
        Normal,
        Tremolo,
        StopTremolo,
        Restart,
        Quit,
        Choreo
    };

    ~Slider() {
        reset();
    }

    Error_t init(int iNodeId, MotorSpec spec) {
        int err = epos.init(iNodeId, spec, kSliderDirection[iNodeId], 5000);
        if (err != 0) {
            LOG_ERROR("Epos init failed for node id: %i", iNodeId);
            return kSetValueError;
        }

        m_iCurrentIdx = kTotalPoints;
        m_mode = Command::Restart;
        Error_t e = home();
        //New Homing Method

        if (e != kNoError) return e;

        m_bInitialized = true;
        return kNoError;
    }

    void reset() {
        epos.reset();
        stopSlide();
        m_bInitialized = false;
    }

    Error_t home() {
        // New
        int err = epos.setOpMode(OpMode::Homing, HomingMethod::CurrentThresholdPositive);
        if (err != 0) {
            LOG_ERROR("setOpMode");
            return kSetValueError;
        }

        err = epos.setEnable();
        if (err != 0) {
            LOG_ERROR("setEnable");
            return kSetValueError;
        }

        err = epos.startHoming();
        if (err != 0) {
            LOG_ERROR("startHoming");
            return kSetValueError;
        }
        //return prepToGoHome();
        int ii = 0;
        bool isHoming = true;
        while (isHoming) {
            isHoming = (epos.getHomingStatus() == InProgress);
            delay(50);
            if (ii++ > 200) break;
        }
        if (epos.getHomingStatus() == Completed) LOG_LOG("Homing complete");
        delay(1000);

        err = epos.setEnable(false);
        if (err != 0) {
            LOG_ERROR("Disable");
            return kSetValueError;
        }

        return kNoError;
    }

    Error_t prepToGoHome() {
//        m_mode = Command::Restart;
//        Error_t err = generateTraj(0);
//        m_iCurrentIdx = 0;
        //New
//        int err = epos.startHoming();
//        if(err != 0)
//        {
//            LOG_LOG("Error: Homing procedure failed. (Code: %d)\n", err);
//            return kSetValueError; //replace with  error: homing process failed
//        }
//        LOG_LOG("Homing Start Status is: %i", epos.getHomingStatus());
        LOG_LOG("Homing Started");

        bool homingAttained = false;
        while(!homingAttained)
        {
            HomingStatus homingStatus = epos.getHomingStatus();
            //delay(100);
            homingStatus = epos.getHomingStatus();
            LOG_LOG("Homing Status is: %i", epos.getHomingStatus());
            switch(homingStatus)
            {
            case Completed:
                homingAttained = true;
                LOG_LOG("Homing Complete");
                break;
            case InProgress:
                LOG_LOG("Homing In-Progress");
            case Interrupted:
                LOG_LOG("Homing Interrupted");
                return kSetValueError; //replace with error: "Homing Interrupted"
            case Error:
                LOG_LOG("Homing Errored");
                return kSetValueError; //replace with Error: "Homing Error"
            }

        }
        //return err;
        //New
        return kNoError;
    }

    // Prepare and return true if should slider, false if shouldn't slide
    bool prepare(Command mode, uint8_t midiVelocity, uint8_t channelPressure) {
        if (!m_bInitialized) return false;

        // If current mode is tremolo
        // If incoming mode is tremolo, dont do anything
        // if incoming mode is different, first stop tremolo
        if (m_mode == Slider::Command::Tremolo) {
            // If mode is already Tremolo, don't generate new traj
            if (mode == m_mode) return false;
            else stopTremolo();
        }

        m_mode = mode;

        if (m_mode == Command::StopTremolo || (m_mode == Command::Tremolo && midiVelocity == 0)) {
            stopTremolo();
            return false;
        }

        if (m_iCurrentIdx <= m_iEndIdx) {
            LOG_WARN("Command arrived early. CurrentIdx: %i, endIdx: %i", m_iCurrentIdx, m_iEndIdx);
            // If a new command arrives, quick stop current motion and start new trajectory
            int e = epos.PDO_quickStop();
            if (e != 0) {
                LOG_ERROR("PDO Quick stop command failed");
            }
        }

        Error_t err = generateTraj(midiVelocity, channelPressure);
        if (err != 0) {
            LOG_ERROR("Error preparing slider %i with mode %i and velocity %i", epos.getNodeId(), mode, midiVelocity);
            return false;
        }

        return true;
    }

    uint8_t getNodeId() const {
        if (!m_bInitialized) return 0;
        return epos.getNodeId();
    }

    void update() {
        if (!m_bInitialized) return;

        // Check if device is in fault state
        if (!epos.isDeviceReady()) {
            stopSlide();
            return;
        }

        // if (m_iCurrentIdx == 0 || m_iCurrentIdx == kTotalPoints - 1) {
        //     LOG_LOG("%i", epos.getCurrentPosition_ticks());
        // }

        if (m_mode == Command::Tremolo) {
            if (m_iCurrentIdx > m_iEndIdx) { // Keep looping after trajectory ends until stop tremolo is called
                m_iCurrentIdx = m_iTremoloStartIdx;
            }
        }
        else {
            if (m_iCurrentIdx > m_iEndIdx) {    // Trajectory complete
                m_iCurrentIdx = MAX_TRAJ_POINTS;
                epos.PDO_rotate(epos.getCurrentPosition_deg(), false);  // keep sending last postion to avoid 0x8250 - RPDO Timeout Error
                return;
            }
        }

        // Serial.print(epos.getNodeId());
        // Serial.print(" ");
        // Serial.print(m_iCurrentIdx);
        // Serial.print(" ");
        // Serial.println(epos.angle2Pos(m_afTraj[m_iCurrentIdx], false));
        int err = epos.PDO_rotate(m_afTraj[m_iCurrentIdx], false);
        ++m_iCurrentIdx;
    }

    Error_t setRxMsg(can_message_t& msg) {
        int err = epos.setRxMsg(msg);
        if (err != 0) return kSetValueError;
        return kNoError;
    }

    Error_t PDO_processMsg(can_message_t& msg) {
        int err = epos.PDO_processMsg(msg);
        if (err != 0) return kSetValueError;
        return kNoError;
    }

    void handleEMCYMsg(can_message_t& msg) {
        epos.handleEMCYMsg(msg);
    }

    Error_t enablePDO(bool bEnable) {
        int err = 0;

        if (bEnable) {
            err = epos.setOpMode(OpMode::CyclicSyncPosition);
            err = epos.setNMTState(NMTState::Operational);
        }
        else {
            err = epos.setNMTState(NMTState::PreOperational);
        }

        if (err != 0) return kSetValueError;

        return kNoError;
    }

    Error_t enable(bool bEnable) {
        int err = epos.setEnable(bEnable);
        if (err != 0) return kSetValueError;

        return kNoError;
    }

    void slide() {
        m_iCurrentIdx = 0;  // This will trigger the update
    }

    void stopSlide() {
        m_iCurrentIdx = MAX_TRAJ_POINTS;   // This will stop the trajectory update
        Util::fill(m_afTraj, MAX_TRAJ_POINTS, 0);  // reset trajectory array
    }

    void shutdown() {
        reset();
    }

    void startTremolo(uint8_t midiVelocity) {
        m_mode = Command::Tremolo;
        m_iCurrentIdx = MAX_TRAJ_POINTS;
        generateTraj(midiVelocity);
        slide();
    }

    void stopTremolo() {
        m_mode = Command::Normal;
        stopSlide();
        m_iTremoloStartIdx = 0;
        m_iEndIdx = MAX_TRAJ_POINTS;
    }

    void checkAndRecover() {
        // This function uses SDO (very expensive). 
        // Dont do anything if device is ready.
        if (epos.isDeviceReady()) return;

        LOG_LOG("Recovering node %i from error %h", epos.getNodeId(), epos.getDeviceError());
        Error_t err = enablePDO(false);
        if (err != kNoError) {
            LOG_ERROR("Node %i: Cannot Disable PDO", epos.getNodeId());
            return;
        }

        int e = epos.clearFault();
        if (e != 0) {
            LOG_ERROR("Node %i: Cannot clear fault", epos.getNodeId());
            return;
        }

        err = enablePDO(true);
        if (err != kNoError) {
            LOG_ERROR("Node %i: Cannot Enable PDO", epos.getNodeId());
            return;
        }

        err = enable(true);
        if (err != kNoError) {
            LOG_ERROR("Node %i: Cannot Enable Device", epos.getNodeId());
            return;
        }
    }

private:
    Epos4 epos;
    bool m_bInitialized = false;
    Command m_mode = Command::Restart;
    static const int kNumPointsForHit = NUM_POINTS_IN_TRAJ_FOR_HIT * PDO_RATE;
    static const int kNumPointsForUp = NUM_POINTS_IN_TRAJ_FOR_UP * PDO_RATE;
    static const int kTotalPoints = kNumPointsForHit + kNumPointsForUp;   // 65ms total with 1ms cycle time -> 65/1
    int m_iCurrentIdx;
    float m_afTraj[MAX_TRAJ_POINTS];
    int m_iEndIdx = kTotalPoints;

    // Tremolo
    int m_iTremoloStartIdx = 0;
    int m_iTremoloEndIdx = 0;

    Error_t generateTraj(uint8_t midiVelocity, uint8_t channelPressure = 0) {
        float q0, qf;

        switch (m_mode) {
        case Command::Restart:
        case Command::StopTremolo:
            q0 = epos.getCurrentPosition_deg();;
            qf = HOME_POSITION;
            Util::interpWithBlend(q0, qf, kTotalPoints, 0.25, m_afTraj);
            m_iEndIdx = kTotalPoints - 1;
            return kNoError;

        case Command::Quit:
            LOG_ERROR("Cannot generate trajectory for mode: {}", (int)m_mode);
            return kTrajectoryError;

        case Command::Choreo:
            q0 = epos.getCurrentPosition_deg();
            qf = choreoPositionMap(channelPressure);
            m_iEndIdx = choreoTimeMap(midiVelocity) - 1;
            // char msg[64];
            // sprintf(msg, "q0: %i, qf: %i, endIdx: %i", (int) (q0 * 100), (int) (qf * 100), m_iEndIdx);
            // Serial.println(msg);
            Util::interpWithBlend(q0, qf, m_iEndIdx + 1, 0.49, m_afTraj);

            return kNoError;

        default:
            break;
        }

        float fInitialPosition_deg, fSlidePosition_deg, fBlend;
        int iNumPtsForHit, iNumPtsForUp;

        velocityMap(midiVelocity, fInitialPosition_deg, fSlidePosition_deg, fBlend);
        timeMap(midiVelocity, iNumPtsForHit, iNumPtsForUp);

        // go to initial position
        q0 = epos.getCurrentPosition_deg();
        qf = fInitialPosition_deg;
        Util::interpWithBlend(q0, qf, iNumPtsForUp, 0.25, m_afTraj);

        // Downward movement
        q0 = fInitialPosition_deg;
        qf = fSlidePosition_deg;
        Util::interpWithBlend(q0, qf, iNumPtsForHit - iNumPtsForUp, fBlend, &m_afTraj[iNumPtsForUp]);

        // upward movement
        q0 = fSlidePosition_deg;
        qf = (m_mode == Command::Tremolo) ? fInitialPosition_deg : HOME_POSITION;
        float blend = (m_mode == Command::Tremolo) ? fBlend : 0.25;
        Util::interpWithBlend(q0, qf, iNumPtsForUp, blend, &m_afTraj[iNumPtsForHit]);
        m_iEndIdx = kTotalPoints - 1;

        return kNoError;
    }

    float choreoPositionMap(uint8_t pressure) {
        pressure = min(MAX_SLIDER_ANGLE_DEG, pressure);
        return (float)pressure;
    }

    int choreoTimeMap(uint8_t midiVelocity) {
        // The higher the velocity, the faster it should reach target
        float m = log2(max(2, midiVelocity)) * 5.f;
        int b = -100;

        return min(MAX_TRAJ_POINTS, (int)round((MAX_TRAJ_POINTS / m)) + b);
    }

    void timeMap(uint8_t midiVelocity, int& iNumPointsForHit, int& iNumPointsForUp) {
        iNumPointsForHit = kNumPointsForHit;
        iNumPointsForUp = kNumPointsForUp;

        if (m_mode == Command::Tremolo) {
            midiVelocity = getCorrectedVelocity(midiVelocity);

            if (midiVelocity == 0)
                return;

            float m = midiVelocity * 0.08;
            int b = 10;
            iNumPointsForHit = (int)round(kNumPointsForHit / m) + b;
            m_iTremoloStartIdx = kNumPointsForUp;
            m_iTremoloEndIdx = min(kTotalPoints, m_iTremoloStartIdx + (2 * iNumPointsForHit));   // Hit and up are symmetric for tremolo
        }
    }

    void velocityMap(uint8_t midiVelocity, float& fInitialPosition, float& fSlidePosition, float& fBlend) {
        /*
        fInitialPosition = midiVelocity * 0.3 + 10;
        fSlidePosition = -midiVelocity * 0.5;
        fBlend = 8.f / max(16, midiVelocity);
        */

        midiVelocity = getCorrectedVelocity(midiVelocity);

        // Mapping from velocity to position and blend
        fInitialPosition = midiVelocity * 0.3 + 10;
        fSlidePosition = -midiVelocity * 0.5;
        fBlend = 8.f / max(16, midiVelocity);

        if (m_mode == Command::Tremolo) {
            fInitialPosition = midiVelocity * 0.1 + 10;
            fSlidePosition = -midiVelocity * 0.3;
        }
    }

    uint8_t getCorrectedVelocity(uint8_t midiVelocity) {
        // Correction for slide command arriving faster than expected
        float timeCorrection = min(1.f, m_iCurrentIdx / (1.f * kTotalPoints));
        return min(127, midiVelocity * sq(timeCorrection));
    }
};

#endif // SLIDER_H