// #socketオブジェクト生成
let socket = io();
// var socket = io.connect('http://' + document.domain + ':' + location.port);
// #サーバとのコネクション確立
socket.on('connect', function() {
    socket.emit('server_echo', {data: 'client connected!'});
});


// #サーバからのメッセージを出力する関数
socket.on('client_echo', function(data) {
    console.log("echo" + ': ' + data.msg);
});