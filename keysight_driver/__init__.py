# Commands for Keysight equipment SCPI interface
# To add or update commands, modify this file only.
COMMANDS = {
    'GET_BFILE_FILE': '[:SOURce]:RADio:XM[:BBG]:BFILe:FILe?',
    'SET_BFILE_FILE': '[:SOURce]:RADio:XM[:BBG]:BFILe:FILe {value}',
    'GET_BFILE_FRAME': '[:SOURce]:RADio:XM[:BBG]:BFILe:FRAMe?',
    'SET_BFILE_FRAME': '[:SOURce]:RADio:XM[:BBG]:BFILe:FRAMe {value}',
    'SET_BFILE_TYPE': '[:SOURce]:RADio:XM[:BBG]:BFILe:TYPe {value}',
    'GET_BFILE_TYPE': '[:SOURce]:RADio:XM[:BBG]:BFILe:TYPe?',
    'GET_DELAY': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:DELay?',
    'SET_DELAY': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:DELay {value}',
    'SET_FOFFSET': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:FOFfset {value}',
    'GET_FOFFSET': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:FOFfset?',
    'SET_FREQUENCY': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:FREQuency {value}',
    'GET_FREQUENCY': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:FREQuency?',
    'SET_POWER': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:POWer {value}',
    'GET_POWER': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:POWer?',
    'GET_STATE': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:STATe?',
    'SET_STATE': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:CARrier1|2|3:STATe {value}',
    'SET_OVERLAY': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:OVERlay {value}',
    'GET_OVERLAY': '[:SOURce]:RADio:XM[:BBG]:ENA|ENB:OVERlay?',
}

__all__ = [
    'COMMANDS'
]
