const questions = [

{
question: "What is 25 × 4 ?",
options: ["80","100","90","110"],
answer: "100"
},

{
question: "What is 18 + 22 ?",
options: ["40","42","38","36"],
answer: "40"
},

{
question: "What is 15 × 6 ?",
options: ["80","90","100","95"],
answer: "90"
},

{
question: "Which number comes next? 2,4,6,8,?",
options: ["9","10","12","14"],
answer: "10"
},

{
question: "50 ÷ 5 = ?",
options: ["8","9","10","12"],
answer: "10"
},

{
question: "Square root of 81?",
options: ["7","8","9","10"],
answer: "9"
},

{
question: "20% of 200 = ?",
options: ["20","30","40","50"],
answer: "40"
},

{
question: "What is 9 × 9 ?",
options: ["72","81","99","91"],
answer: "81"
},

{
question: "100 - 37 = ?",
options: ["63","73","53","67"],
answer: "63"
},

{
question: "Which is the largest?",
options: ["21","18","35","29"],
answer: "35"
}

];

let currentQuestion = 0;
let score = 0;

const questionText = document.getElementById("question");
const optionsDiv = document.getElementById("options");
const questionNumber = document.getElementById("questionNumber");
const nextBtn = document.getElementById("nextBtn");

function loadQuestion(){

let q = questions[currentQuestion];

questionNumber.innerHTML =
"Question " + (currentQuestion+1) + " of " + questions.length;

questionText.innerHTML = q.question;

optionsDiv.innerHTML="";

q.options.forEach(option=>{

optionsDiv.innerHTML += `
<label>
<input type="radio" name="option" value="${option}">
${option}
</label>
`;

});

if(currentQuestion==questions.length-1){

nextBtn.innerHTML="Submit Test";

}else{

nextBtn.innerHTML="Next";

}

}

loadQuestion();

nextBtn.addEventListener("click",function(){

let selected=document.querySelector('input[name="option"]:checked');

if(!selected){

alert("Please select an answer.");

return;

}

if(selected.value===questions[currentQuestion].answer){

score++;

}

currentQuestion++;

if(currentQuestion<questions.length){

loadQuestion();

}else{

fetch("/save_score", {

    method: "POST",

    headers: {
        "Content-Type": "application/json"
    },

    body: JSON.stringify({

        score: score,

        total: questions.length

    })

})
.then(response => response.json())
.then(data => {

    if(data.status === "success"){

        alert("🎉 Test Completed!\n\nYour Score: " + score + " / " + questions.length);

        window.location.href = "/dashboard";

    }else{

        alert("Error saving score!");

    }

});

}

});