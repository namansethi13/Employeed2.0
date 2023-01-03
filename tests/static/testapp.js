window.addEventListener('blur', pause);

let url = 'ws://127.0.0.1:8000/ws/test-socket/'

const testSocket = new WebSocket(url)

testSocket.onmessage = function(e){
    console.log("Received something")
    let data = JSON.parse(e.data)
    console.log('Data ', data)

    if(data.type == 'submit'){
        console.log("submit the test!")

        document.getElementById("testform").submit();

    }

    if(data.type == 'markQuestion'){
        console.log("inside");
        let questionList = data.questionList
        let i = 1
        questionList.forEach(element => {
            $('input:radio[name="'+ i + '"]').filter('[value="'+ element + '"]').attr('checked', true);
            i++;
        });
  
        // This will select the radio button
    }
}



let current = 0;
let totalQ = document.getElementsByClassName("question").length;
let flagBtn = document.getElementById("flagBtn");
function flagtext(question){
    if(question<0){
        return;
    }
   if(question.flagged){
        flagBtn.value= "unflag question";
    }
    else{
        flagBtn.value= "flag question";
    }
}
class question{
    
    constructor(question) {
        this.allQuestions = document.getElementsByClassName("question");
        this.question = question.children[0].innerHTML;
        this.index = question.getAttribute("indexnum");
        this.A = A;
        this.B = B;
        this.C = C;
        this.D = D;
        this.flagged = false;
        //indexing question
        let btn = document.createElement("button");
        let btntext = document.createTextNode(this.index);
        btn.classList.add("qBtn");
        btn.setAttribute("type","button");
        btn.appendChild(btntext);
        this.Ibutton = btn;
        question.setAttribute("id","questionHidden")
        document.getElementById("indexWrapper").appendChild(btn);

        btn.onclick = () =>{
            
                 current = this.index;
                 for (const element of this.allQuestions ) {
                     element.setAttribute("id","questionHidden");
                    
                 }
                
                 question.setAttribute("id","");

                flagtext(questionObjList[current-1]);
                
             }
    }

    nextQuestion(question){
        current = this.index;
        for (const element of this.allQuestions ) {
            element.setAttribute("id","questionHidden");
            
        }
        
        question.setAttribute("id","")
                         flagtext(questionObjList[current-1]);

        
    }


    buttonclass(className){
        this.Ibutton.setAttribute("class",className);
    }

    


}

function pause(){ 
//   alert("Alert! You have got a warning for switching tabs 3 of those may result in test cancelation");

    $.ajaxSetup({
        headers: {
            // "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            "X-CSRFToken": "demo token", //this line will be removed the line above will be used
        }
    });
    $.ajax({
    url: 'warning',
    method: 'POST',
    data: {
      'warning_type': "tab_switched"
    },
    dataType: 'json',
    success: function (data) {
      alert(data.warningType+" you have got a warning after "+data.warningLeft+" test will be canceled")
    }
  });
};

let nextBtn = document.getElementById("nextBtn");

nextBtn.onclick = () => {
    if(current < totalQ){
        current++;
        questionObjList[current-1].nextQuestion(questions[current-1]);
    }

    return;
}
let questions= document.getElementsByClassName("question");
let questionObjList = [];
for (const quest of questions ) {
    let tempQ = new question(quest);
    questionObjList.push(tempQ);

  }


flagBtn.onclick = () => {
    if(current-1<0){
        return;
    }
    if(questionObjList[current-1].flagged){
        questionObjList[current-1].flagged = false;
        questionObjList[current-1].buttonclass("qBtn")
        flagtext(questionObjList[current-1])
        return;
    }
    
    questionObjList[current-1].flagged = true;
    questionObjList[current-1].buttonclass("qBtnFlagged")
    flagtext(questionObjList[current-1])

    return



  }



//views.py file

// def warning(request):
//     if request.POST['warning_type'] == 'tab_switched
//     data = {
//         'warningType' : 'tab switched'
//     }
//     return JsonResponse(data)


function getquestion(){
    $.ajaxSetup({
        headers: {
            // "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            "X-CSRFToken": "demo token", //this line will be removed the line above will be used
            "getData" : true
        }
    });
    $.ajax({
    url: 'questionlog',
    method: 'POST',
    data: { },
    dataType: 'json',
    success: function (data) {
        // $('input:radio[name=""]').filter('[value=""]').attr('checked', true);
        // handle data
    }
  });
  }
  
  function getData(){
      data = { "type" : "getquestion",}

  testSocket.send(JSON.stringify(data))
  }



let intervalId = window.setInterval(function(){
    let questionLogList = [];
    for(let i = 1 ; i != totalQ+1 ; i++){

        let temp = $('input[name="'+i+'"]:checked').val();
        questionLogList.push(temp);


    }
    getData();
    console.log(questionLogList);
    

    data = { "type" : "question_list",
        "questionList" : questionLogList }

    testSocket.send(JSON.stringify(data))


    }, 10000);







//remove all the flagged fields 


 //submit ajax response
 //every 10 second request
 // websocket timer