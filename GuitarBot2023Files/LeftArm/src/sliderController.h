//
//
//

#ifndef SLIDERCONTROLLER_H
#define SLIDERCONTROLLER_H

#include "def.h"
#include "slider.h"
#include <HardwareTimer.h>

class SliderController {
public:
    static SliderController* createInstance() {
        pInstance = new SliderController;
        return pInstance;
    }

    static void destroyInstance() {
        delete pInstance;
        pInstance = nullptr;
    }

    Error_t init(MotorSpec spec, bool bInitCAN = true) {
        int err = 0;
        
        if (bInitCAN) {
            if (!CanBus.begin(CAN_BAUD_500K, CAN_STD_FORMAT)) {
                LOG_ERROR("CAN open failed");
                return kFileOpenError;
            }

            CanBus.attachRxInterrupt(canRxHandle);
        }

        RPDOTimer.setPeriod(PDO_RATE * 1000);
        RPDOTimer.attachInterrupt(RPDOTimerIRQHandler);

        // faultClearTimer.setPeriod(CLEAR_FAULT_TIMER_INTERVAL * 1000);
        // faultClearTimer.attachInterrupt(clearFaultTimerIRQHandler);

        return initSliders(spec);
    }

    Error_t initSliders(MotorSpec spec) {
        m_motorSpec = spec;
        Error_t err = kNoError;
        for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
            err = m_slider[i].init(i, spec);
            if (err != kNoError) {
                LOG_ERROR("Cannot initialize slider with id %i. Error: %i", i, err);
            }
        }

        return kNoError;
    }

    Error_t resetSliders() {
        enablePDO(false);
        for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
            m_slider[i].reset();
        }
    }

    void reset(bool bTerminateCAN = true) {
        m_bPlaying = false;
        RPDOTimer.stop();
        // faultClearTimer.stop();
        auto err = resetSliders();
        if (err != kNoError) {
            LOG_ERROR("Cannot reset sliders");
        }
        if (bTerminateCAN)
            CanBus.end();
    }



    Slider::Command getSliderMode(char mode) {
        switch (mode) {
        case 's':
            return Slider::Command::Normal;
        //case 't':
        //    return Slider::Command::Tremolo;
        case 'r':
            return Slider::Command::Restart;
        case 'q':
            return Slider::Command::Quit;
        //case 'c':
        //    return Slider::Command::Choreo;
        default:
            LOG_ERROR("unknown command : %i", mode);
            return Slider::Command::Normal;
        }
    }

    //what to do with midiVelocity? Are these params all needed?
    uint8_t prepare(uint8_t idCode, char mode, uint8_t midiVelocity, uint8_t channelPressure) {
        return prepare(idCode, getSliderMode(mode), midiVelocity, channelPressure);
    }

    Error_t restart() {
        auto spec = m_motorSpec;
        reset(false);
        Error_t err = init(spec, false);
        if (err != kNoError) {
            LOG_ERROR("Cannot init controller");
            return err;
        }

        start();

        return kNoError;
    }

    //what to do with midiVelocity? All params needed?
    uint8_t prepare(uint8_t idCode, Slider::Command mode, uint8_t midiVelocity, uint8_t channelPressure) {
        uint8_t uiSlide = 0;

        switch (mode) {
        case Slider::Command::Restart:
            restart();
            break;

        case Slider::Command::Quit:
            for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
                m_slider[i].shutdown();
            }
            break;

        default:
            for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
                if (idCode & (1 << (i - 1))) {
                    bool bSlide = m_slider[i].prepare(mode, midiVelocity, channelPressure);
                    uiSlide += bSlide << (i - 1);
                }
            }
        }

        return uiSlide;
    }

    void executeCommand(uint8_t idCode, char mode, uint8_t midiVelocity, uint8_t channelPressure) {
        uint8_t uiSlide = prepare(idCode, mode, midiVelocity, channelPressure);
        slide(uiSlide);
    }

    void start() {
        Error_t err = enablePDO();
        if (err != kNoError) {
            LOG_ERROR("cannot enable PDO");
            return;
        }

        err = enableSliders();
        if (err != kNoError) {
            LOG_ERROR("cannot enable Sliders");
            return;
        }

        m_bPlaying = true;
        RPDOTimer.start();
        // faultClearTimer.start();
    }

    void stop() {
        Error_t err;
        err = enablePDO(false);
        if (err != kNoError) {
            LOG_ERROR("cannot disable PDO");
            return;
        }

        err = enableSliders(false);
        if (err != kNoError) {
            LOG_ERROR("cannot disable Sliders");
            return;
        }

        m_bPlaying = false;
        RPDOTimer.stop();
        // faultClearTimer.stop();
    }

    Error_t enablePDO(bool bEnable = true) {
        Error_t err;
        for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
            err = m_slider[i].enablePDO(bEnable);
            if (err != kNoError) {
                LOG_ERROR("EnablePDO failed. Error Code %i", err);
                return err;
            }
        }

        return kNoError;
    }

    Error_t enableSliders(bool bEnable = true) {
        int err;
        for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
            err = m_slider[i].enable(bEnable);
            if (err != 0) {
                LOG_ERROR("Enable failed. Error Code %h", err);
                return kSetValueError;
            }
        }

        return kNoError;
    }

    int slide(uint8_t idCode) {
        for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
            if (idCode & (1 << (i - 1))) {
                // LOG_LOG("(idcode: %h) Striking: %i", idCode, i);
                m_slider[i].slide();
            }
        }
    }

private:
    Slider m_slider[NUM_SLIDERS + 1]; // 0 is dummy
    static SliderController* pInstance;
    volatile bool m_bPlaying = false;
    MotorSpec m_motorSpec = MotorSpec::EC45;

    HardwareTimer RPDOTimer;//, faultClearTimer;

    SliderController() : RPDOTimer(TIMER_CH1) {}
    // , faultClearTimer(TIMER_CH3) {}

    ~SliderController() {
        reset();
        destroyInstance();
    }

    static void canRxHandle(can_message_t* arg) {
        auto id = arg->id - COB_ID_SDO_SC;
        if (id > 0 && id < NUM_SLIDERS + 1) {
            pInstance->m_slider[id].setRxMsg(*arg);
        }

        id = arg->id - COB_ID_TPDO3;
        if (id > 0 && id < NUM_SLIDERS + 1) {
            pInstance->m_slider[id].PDO_processMsg(*arg);
        }

        id = arg->id - COB_ID_EMCY;
        if (id > 0 && id < NUM_SLIDERS + 1) {
            pInstance->m_slider[id].handleEMCYMsg(*arg);
        }
    }

    static void RPDOTimerIRQHandler() {
        for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
            pInstance->m_slider[i].update();
        }
    }

    // static void clearFaultTimerIRQHandler() {
    //     for (int i = 1; i < NUM_SLIDERS + 1; ++i) {
    //         pInstance->m_slider[i].checkAndRecover();
    //     }
    // }
};

SliderController* SliderController::pInstance = nullptr;
#endif // SLIDERCONTROLLER_H