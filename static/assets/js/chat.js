function getCookie(name){
    var cookieValue = null;
    if (document.cookie && document.cookie !== ''){
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++){
            var cookie = jQuery.trim(cookies[i]);
            if(cooke.substring(0,name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
var xhr;

function enterkey() {
    if (window.event.keyCode == 13) {
        sendAsk();
    }
    return
}

function nowTime(){
    var today = new Date();
    var hours = today.getHours(); // 시
    var minutes = today.getMinutes();  // 분

    hours = hours + ''
    minutes = minutes + ''

    if (hours.length == 1){
        hours = '0' + hours
    }
    if (minutes.length == 1){
        minutes = '0' + minutes
    }
    return ' ' + hours + ' : ' + minutes;
}

function sendAsk(){
//    <!--  input 받음  -->
    var chattext = $('#inputId').val();
//    console.log(chattext)
    checktxt = '<div class="chats chats-right"><div class="chat-content"><div class="message-content">'
                + '<div class="user-msg">' + chattext + '</div>' +
                '<div class="chat-time"><div><div class="time"><i class="fas fa-clock"></i>'
                + nowTime() +
                '</div></div></div></div><div class="chat-profile-name text-right"><h6>Me</h6></div></div>'
                + '<div class="chat-action-btns mr-2"><div class="chat-read-col"><span class="material-icons">done_all</span></div></div></div>'

    document.getElementById("messages").innerHTML += checktxt;



    <!--    챗봇 대답 요청    -->
//    var strurl = "chatanswer?questext=" + chattext;
    var strurl = "chatanswer?questext=" + chattext;
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            var data = xhr.responseText;
            console.log(data)
            var obj = JSON.parse(data);

            if(obj.flag == "0"){
                // checker = "<div style='color:red'>" + obj.checker + "<div>"
                // document.getElementById("messages").innerHTML += checker

                bottext = '<div class="chats"><div class="chat-avatar"><img src="static/assets/img/avatar_friends/rachelgreen.jpg" class="rounded-circle dreams_chat" alt="image">" </div> <div class="chat-content"><div class="message-content">'
                        + obj.anstext +
                        '<div class="chat-time"><div><div class="time"><i class="fas fa-clock"></i>'
                        + nowTime() +
                        '</div></div></div></div><div class="chat-profile-name"><h6>Rachel Green</h6></div></div></div>'

                document.getElementById("messages").innerHTML += bottext;

                var objDiv = document.getElementById("messages");
                objDiv.scrollTop = objDiv.scrollHeight;

                document.getElementById("messages").value = "";
                document.getElementById("messages").focus();

            }
        }
    };
    xhr.open("GET", strurl);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(null);
    $('#inputId').val('');
}

function checkGrammar(){
<!--   문법 교정 api 작동     -->
    var inputs = document.getElementsByClassName("user-msg")
    var len = inputs.length

//    console.log('len : ',len)
//    console.log('inputs : ', inputs)

    for (var inpIdx = 0; inpIdx < len; inpIdx++){
        // console.log(inputs[inpIdx].innerText)
        var text = inputs[inpIdx].innerText
//        console.log('text' , text)

        // console.log(text)
        var settings = {
            "async": false,
            "crossDomain": true,
            "url": "https://dnaber-languagetool.p.rapidapi.com/v2/check",
            "method": "POST",
            "headers": {
                "content-type": "application/x-www-form-urlencoded",
                "x-rapidapi-host": "dnaber-languagetool.p.rapidapi.com",
                "x-rapidapi-key": "49491d0e58mshc6937e8d420377ap1de6f6jsn6ea9c2dcaa0b"
            },
            "data": {
                "text": text,
                "language": "en-US"
            }
        };

        var res;

        $.ajax(settings).done(function (response) {
            var length = []
            var offset = []
            var color_list = []
            var rt_msg_all = []
            // console.log(response);
            matches = response.matches

            if (matches.length === 0) {
                // 맞는 문장
                rt_msg = ""
                console.log("correct!")
                return
            }
            else{
                // 틀린 문장
                // 오류가 여러 개면 여러 개 출력
                // console.log(matches.length)
                for (var m = 0; m < matches.length; m++){
                    var colors;
                    rt_msg = ""
                    err = matches[m].shortMessage;
                    if (err == 'Spelling mistake') {
                        rt_msg += "There is a spelling mistake.<br>The chatbot may not work smoothly.<br>"
                        colors = "#AEB1FF"
                    }
                    else if (err == ''){
                        continue
                    }
                    else{
                        rt_msg += err + " : " + matches[m].message + "<br>"
                        rt_msg += "Can be replaced by : "
                        rep = matches[m].replacements
                        for (var i = 0; i < rep.length; i++){
                            rt_msg += rep[i].value
                            if (i != rep.length - 1){
                                rt_msg += ','
                            }
                        }
                        rt_msg += "<br>"
                        colors = "pink"
                    }

                    rt_msg_all.push(rt_msg)
                    context = response.matches[m].context
                    length.push(context.length)
                    offset.push(context.offset)
                    color_list.push(colors)

                    console.log('rt_msg')
                    console.log(rt_msg_all)


                }

                if (rt_msg_all.length === 0){
                    return
                }

                var hl = ""
                for (var idx = 0; idx<offset.length; idx++ ){
                    if (idx == 0){
                        hl += "<span>"+text.slice(0, offset[idx])+"</span>"
                    }
                    hl += "<span class='gc-tooltip' style='background-color:" + color_list[idx] + "'>" + text.slice(offset[idx], offset[idx]+length[idx]) +
                            "<span class='gc-tooltiptext'>"+rt_msg_all[idx]+"</span>"+"</span>"
                    if (idx == offset.length - 1){
                        hl += "<span>"+text.slice(offset[idx]+length[idx])+"</span>"
                    }
                    else{
                        hl += "<span>"+text.slice(offset[idx]+length[idx], offset[idx+1])+"</span>"
                    }
                }
//                console.log('inpidx',inpIdx)
                $($('.user-msg')[inpIdx]).html(hl)

            }

        });

    }
}
