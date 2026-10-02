import HistorySamplingSemantics
set_option maxRecDepth 20000
namespace Orthemology.RuntimeBridge.HistoryRuntime
open P02.Codec
#eval IO.println ("HISTORY_BYTES_0=" ++ "[" ++ String.intercalate ","
  ((encodeBytes (Natural.compiled (nextProgram selectorProgram false)
    (outputProgram selectorProgram false) initial)).map toString) ++ "]")
#eval IO.println ("HISTORY_INDEX_0=" ++ toString (runtimeIndex selectorProgram false))
#eval IO.println ("HISTORY_BYTES_1=" ++ "[" ++ String.intercalate ","
  ((encodeBytes (Natural.compiled (nextProgram selectorProgram true)
    (outputProgram selectorProgram true) initial)).map toString) ++ "]")
#eval IO.println ("HISTORY_INDEX_1=" ++ toString (runtimeIndex selectorProgram true))
end Orthemology.RuntimeBridge.HistoryRuntime
