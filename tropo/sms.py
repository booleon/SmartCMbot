# How to Call via API Token
# https://api.tropo.com/1.0/sessions?action=create&token=516b787555467055586f63625a754270414e714264506b704c715a6e7578575474545051745a4175676d7177&cNumber=+33685651240&cAnswer=MyMessageIsHere

if(currentCall) :
    if(currentCall.initialText == "Echo") :
        message("This is an echo.", {"to":"+16467413875", "network":"SMS"})
    else :
        message(currentCall.initialText , {"to":"+16467413875", "network":"SMS"})
    
else :
    call(cNumber, {"network":"SMS"})
    say(cAnswer)