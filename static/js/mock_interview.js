const questions = [
    "Tell me about yourself.",
    "What are your strengths?",
    "What are your weaknesses?",
    "Why should we hire you?",
    "Where do you see yourself in five years?"
];

let current = 0;
let score = 0;

const question = document.getElementById("question");
const answer = document.getElementById("answer");

document.getElementById("nextBtn").onclick = function(){

    if(answer.value.trim().length > 30){
        score += 20;
    }

    current++;

    if(current < questions.length){

        question.innerHTML = questions[current];
        answer.value = "";

    }else{

        fetch("/interview_score",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                score:score
            })

        })
        .then(res=>res.json())
        .then(data=>{

            alert(
                "Interview Completed!\n\nScore : "
                + data.score +
                "%\n\nFeedback : " +
                data.feedback
            );

            window.location.href="/dashboard";

        });

    }

};