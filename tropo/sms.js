if (currentCall) {
    choice = currentCall.initialText.toLowerCase();
    if ((choice.startsWith("echo")) || (choice.startsWith("eco")))  
    {
        message("This is an echo.", {"to":"+16467413875", "network":"SMS"});
    }
    else 
    {
        message(currentCall.initialText , {"to":"+16467413875", "network":"SMS"});
    }
}
else {
    call(cNumber, { "network":"SMS" });
    say(cAnswer);
}
