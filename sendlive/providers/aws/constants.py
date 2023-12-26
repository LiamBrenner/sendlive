from typing import Any

DEFAULT_ORIGIN_ENDPOINT_HLS_PACKAGE: dict[str, Any] = {
    "adMarkers": "NONE",
    "adTriggers": [
        "SPLICE_INSERT",
        "PROVIDER_ADVERTISEMENT",
        "DISTRIBUTOR_ADVERTISEMENT",
        "PROVIDER_PLACEMENT_OPPORTUNITY",
        "DISTRIBUTOR_PLACEMENT_OPPORTUNITY",
    ],
    "adsOnDeliveryRestrictions": "RESTRICTED",
    "includeIframeOnlyStream": False,
    "playlistType": "EVENT",
    "playlistWindowSeconds": 60,
    "programDateTimeIntervalSeconds": 0,
    "segmentDurationSeconds": 4,
    "streamSelection": {"streamOrder": "ORIGINAL"},
    "useAudioRenditionGroup": False,
}

# Medialive

DEFAULT_MEDIALIVE_ENCODER_SETTINGS: dict[str, Any] = {
    "audioDescriptions": [
        {
            "audioSelectorName": "Default",
            "audioTypeControl": "FOLLOW_INPUT",
            "codecSettings": {
                "aacSettings": {
                    "bitrate": 128000,
                    "codingMode": "CODING_MODE_2_0",
                    "inputType": "NORMAL",
                    "profile": "LC",
                    "rateControlMode": "CBR",
                    "rawFormat": "NONE",
                    "sampleRate": 48000,
                    "spec": "MPEG4",
                }
            },
            "languageCodeControl": "FOLLOW_INPUT",
            "name": "audio_0",
        },
        {
            "audioSelectorName": "Default",
            "audioTypeControl": "FOLLOW_INPUT",
            "codecSettings": {
                "aacSettings": {
                    "bitrate": 128000,
                    "codingMode": "CODING_MODE_2_0",
                    "inputType": "NORMAL",
                    "profile": "LC",
                    "rateControlMode": "CBR",
                    "rawFormat": "NONE",
                    "sampleRate": 48000,
                    "spec": "MPEG4",
                }
            },
            "languageCodeControl": "FOLLOW_INPUT",
            "name": "audio_1",
        },
        {
            "audioSelectorName": "Default",
            "audioTypeControl": "FOLLOW_INPUT",
            "codecSettings": {
                "aacSettings": {
                    "bitrate": 128000,
                    "codingMode": "CODING_MODE_2_0",
                    "inputType": "NORMAL",
                    "profile": "LC",
                    "rateControlMode": "CBR",
                    "rawFormat": "NONE",
                    "sampleRate": 48000,
                    "spec": "MPEG4",
                }
            },
            "languageCodeControl": "FOLLOW_INPUT",
            "name": "audio_2",
        },
        {
            "audioSelectorName": "Default",
            "audioTypeControl": "FOLLOW_INPUT",
            "codecSettings": {
                "aacSettings": {
                    "bitrate": 128000,
                    "codingMode": "CODING_MODE_2_0",
                    "inputType": "NORMAL",
                    "profile": "LC",
                    "rateControlMode": "CBR",
                    "rawFormat": "NONE",
                    "sampleRate": 48000,
                    "spec": "MPEG4",
                }
            },
            "languageCodeControl": "FOLLOW_INPUT",
            "name": "audio_3",
        },
    ],
    "globalConfiguration": {
        "outputLockingMode": "PIPELINE_LOCKING",
        "outputTimingSource": "INPUT_CLOCK",
        "supportLowFramerateInputs": "DISABLED",
    },
    "outputGroups": [
        {
            "outputGroupSettings": {
                "mediaPackageGroupSettings": {
                    "destination": {"destinationRefId": "changeme"}
                }
            },
            "outputs": [
                {
                    "audioDescriptionNames": ["audio_0"],
                    "outputName": "emp_1080p25",
                    "outputSettings": {"mediaPackageOutputSettings": {}},
                    "videoDescriptionName": "emp_1080p25",
                },
                {
                    "audioDescriptionNames": ["audio_1"],
                    "outputName": "emp_720p25",
                    "outputSettings": {"mediaPackageOutputSettings": {}},
                    "videoDescriptionName": "emp_720p25",
                },
                {
                    "audioDescriptionNames": ["audio_2"],
                    "outputName": "emp_480p25",
                    "outputSettings": {"mediaPackageOutputSettings": {}},
                    "videoDescriptionName": "emp_480p25",
                },
                {
                    "audioDescriptionNames": ["audio_3"],
                    "outputName": "emp_240p25",
                    "outputSettings": {"mediaPackageOutputSettings": {}},
                    "videoDescriptionName": "emp_240p25",
                },
            ],
        }
    ],
    "timecodeConfig": {"source": "SYSTEMCLOCK"},
    "videoDescriptions": [
        {
            "codecSettings": {
                "h264Settings": {
                    "adaptiveQuantization": "HIGH",
                    "afdSignaling": "NONE",
                    "bitrate": 5000000,
                    "colorMetadata": "INSERT",
                    "entropyEncoding": "CABAC",
                    "flickerAq": "ENABLED",
                    "forceFieldPictures": "DISABLED",
                    "framerateControl": "SPECIFIED",
                    "framerateDenominator": 1,
                    "framerateNumerator": 25,
                    "gopBReference": "ENABLED",
                    "gopClosedCadence": 1,
                    "gopNumBFrames": 5,
                    "gopSize": 1.92,
                    "gopSizeUnits": "SECONDS",
                    "level": "H264_LEVEL_AUTO",
                    "lookAheadRateControl": "HIGH",
                    "maxBitrate": 5000000,
                    "numRefFrames": 3,
                    "parControl": "SPECIFIED",
                    "parDenominator": 1,
                    "parNumerator": 1,
                    "profile": "MAIN",
                    "rateControlMode": "QVBR",
                    "scanType": "PROGRESSIVE",
                    "sceneChangeDetect": "ENABLED",
                    "slices": 1,
                    "spatialAq": "ENABLED",
                    "subgopLength": "DYNAMIC",
                    "syntax": "DEFAULT",
                    "temporalAq": "ENABLED",
                    "timecodeInsertion": "DISABLED",
                }
            },
            "height": 1080,
            "name": "emp_1080p25",
            "respondToAfd": "NONE",
            "scalingBehavior": "DEFAULT",
            "sharpness": 50,
            "width": 1920,
        },
        {
            "codecSettings": {
                "h264Settings": {
                    "adaptiveQuantization": "HIGH",
                    "afdSignaling": "NONE",
                    "bitrate": 3000000,
                    "colorMetadata": "INSERT",
                    "entropyEncoding": "CABAC",
                    "flickerAq": "ENABLED",
                    "forceFieldPictures": "DISABLED",
                    "framerateControl": "SPECIFIED",
                    "framerateDenominator": 1,
                    "framerateNumerator": 25,
                    "gopBReference": "ENABLED",
                    "gopClosedCadence": 1,
                    "gopNumBFrames": 5,
                    "gopSize": 1.92,
                    "gopSizeUnits": "SECONDS",
                    "level": "H264_LEVEL_AUTO",
                    "lookAheadRateControl": "HIGH",
                    "maxBitrate": 3000000,
                    "numRefFrames": 3,
                    "parControl": "SPECIFIED",
                    "parDenominator": 1,
                    "parNumerator": 1,
                    "profile": "MAIN",
                    "rateControlMode": "QVBR",
                    "scanType": "PROGRESSIVE",
                    "sceneChangeDetect": "ENABLED",
                    "slices": 1,
                    "spatialAq": "ENABLED",
                    "subgopLength": "DYNAMIC",
                    "syntax": "DEFAULT",
                    "temporalAq": "ENABLED",
                    "timecodeInsertion": "DISABLED",
                }
            },
            "height": 720,
            "name": "emp_720p25",
            "respondToAfd": "NONE",
            "scalingBehavior": "DEFAULT",
            "sharpness": 75,
            "width": 1280,
        },
        {
            "codecSettings": {
                "h264Settings": {
                    "adaptiveQuantization": "HIGH",
                    "afdSignaling": "NONE",
                    "bitrate": 1500000,
                    "colorMetadata": "INSERT",
                    "entropyEncoding": "CABAC",
                    "flickerAq": "ENABLED",
                    "forceFieldPictures": "DISABLED",
                    "framerateControl": "SPECIFIED",
                    "framerateDenominator": 1,
                    "framerateNumerator": 25,
                    "gopBReference": "ENABLED",
                    "gopClosedCadence": 1,
                    "gopNumBFrames": 5,
                    "gopSize": 1.92,
                    "gopSizeUnits": "SECONDS",
                    "level": "H264_LEVEL_AUTO",
                    "lookAheadRateControl": "HIGH",
                    "maxBitrate": 1500000,
                    "numRefFrames": 3,
                    "parControl": "SPECIFIED",
                    "parDenominator": 1,
                    "parNumerator": 1,
                    "profile": "MAIN",
                    "rateControlMode": "QVBR",
                    "scanType": "PROGRESSIVE",
                    "sceneChangeDetect": "ENABLED",
                    "slices": 1,
                    "spatialAq": "ENABLED",
                    "subgopLength": "DYNAMIC",
                    "syntax": "DEFAULT",
                    "temporalAq": "ENABLED",
                    "timecodeInsertion": "DISABLED",
                }
            },
            "height": 480,
            "name": "emp_480p25",
            "respondToAfd": "NONE",
            "scalingBehavior": "STRETCH_TO_OUTPUT",
            "sharpness": 100,
            "width": 854,
        },
        {
            "codecSettings": {
                "h264Settings": {
                    "adaptiveQuantization": "HIGH",
                    "afdSignaling": "NONE",
                    "bitrate": 750000,
                    "colorMetadata": "INSERT",
                    "entropyEncoding": "CABAC",
                    "flickerAq": "ENABLED",
                    "forceFieldPictures": "DISABLED",
                    "framerateControl": "SPECIFIED",
                    "framerateDenominator": 1,
                    "framerateNumerator": 25,
                    "gopBReference": "ENABLED",
                    "gopClosedCadence": 1,
                    "gopNumBFrames": 5,
                    "gopSize": 1.92,
                    "gopSizeUnits": "SECONDS",
                    "level": "H264_LEVEL_AUTO",
                    "lookAheadRateControl": "HIGH",
                    "maxBitrate": 750000,
                    "numRefFrames": 3,
                    "parControl": "SPECIFIED",
                    "parDenominator": 1,
                    "parNumerator": 1,
                    "profile": "MAIN",
                    "rateControlMode": "QVBR",
                    "scanType": "PROGRESSIVE",
                    "sceneChangeDetect": "ENABLED",
                    "slices": 1,
                    "spatialAq": "ENABLED",
                    "subgopLength": "DYNAMIC",
                    "syntax": "DEFAULT",
                    "temporalAq": "ENABLED",
                    "timecodeInsertion": "DISABLED",
                }
            },
            "height": 240,
            "name": "emp_240p25",
            "respondToAfd": "NONE",
            "scalingBehavior": "STRETCH_TO_OUTPUT",
            "sharpness": 100,
            "width": 426,
        },
    ],
}

MEDIALIVE_DEFAULT_INPUT_SPEC: dict[str, Any] = {
    "codec": "AVC",
    "maximumBitrate": "MAX_20_MBPS",
    "resolution": "HD",
}


DEFAULT_MEDIALIVE_CHANNEL_PARAMS: dict[str, Any] = {
    "channelClass": "SINGLE_PIPELINE",
    "destinations": [
        {
            "id": "changeme",
            "mediaPackageSettings": [{"channelId": "changeme"}],
        }
    ],
    "encoderSettings": DEFAULT_MEDIALIVE_ENCODER_SETTINGS,
    "inputAttachments": [
        {
            "inputAttachmentName": "changeme",
            "inputId": "changeme",
            "inputSettings": {
                "deblockFilter": "DISABLED",
                "denoiseFilter": "DISABLED",
                "filterStrength": 1,
                "inputFilter": "AUTO",
                "smpte2038DataPreference": "IGNORE",
                "sourceEndBehavior": "CONTINUE",
            },
        }
    ],
    "inputSpecification": MEDIALIVE_DEFAULT_INPUT_SPEC,
    "name": "changeme",
}
