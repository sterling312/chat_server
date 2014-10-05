var onopen = function (){
    $('div#window div').remove();
}

var onmessage = function (evt){
    var $div = $('<div></div>').text(evt.data);
    $('div#window').append($div);
}

var ws;
function open_ws(data){
    var params = $.param({username:data.username});
    ws = new WebSocket(data.url+'?'+params);
    ws.onopen = onopen;
    ws.onmessage = onmessage;
}

function login(username){
    var params = $.param({username:username});
    $.ajax('/url?'+params,{
        method:'get',
        dataType:'json',
    }).done(open_ws);
}

$(document).ready(function(){
    $('div.chat').hide();
    $('button#send').click(function(){
        var $text = $('input#message');
        ws.send($text.val());
        $text.val('');
    });

    $('button#login').click(function(){
        var $user = $('input#username');
        if ($user.val()){
            login($user.val());
        };
        $('div.login').hide();
        $('div.chat').show();
    });
});
