function sendMessage(){

    let input = document.getElementById("userInput");

    let message = input.value.trim();

    if(message=="") return;

    let chat = document.getElementById("chat-box");

    chat.innerHTML += "<p><b>You:</b> "+message+"</p>";

    let reply = "";

    message = message.toLowerCase();

    if(message.includes("python")){

        reply = "Python is a beginner-friendly programming language used in AI, ML and Web Development.";

    }

    else if(message.includes("interview")){

        reply = "Practice aptitude, coding, HR questions and mock interviews regularly.";

    }

    else if(message.includes("resume")){

        reply = "Keep your resume to one page and highlight projects and skills.";

    }

    else{

        reply = "I'm still learning. Please ask about Python, resume or interviews.";

    }

    chat.innerHTML += "<p><b>PrepAI:</b> "+reply+"</p>";

    input.value="";

    chat.scrollTop = chat.scrollHeight;

}