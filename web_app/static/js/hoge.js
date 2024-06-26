var hoge = document.querySelectorAll('#result_items p') 
for(var ele of hoge) {
    
    if (ele.innerHTML == 'None') {
        ele.hidden = true;
    } else {
        console.log("textid: " + ele.innerHTML);
    }
}

// jsをパース後に読み込む時はonload関数を使うかdefer属性を使用
var ele = document.getElementById('hoge');
console.log('hello: ' + ele);
console.log('hello: ' + ele.innerText);

// onload関数は特性上最後に処理実行
window.onload = function(){
    console.log('以降onload関数')
    console.log('hello: ' + ele);
    console.log('hello: ' + ele.innerText);
}

// addEventListenerはonload関数の内外関係なく動く
var ele2 = document.getElementById('fuga');
console.log('event: ' + ele2);
ele2.addEventListener('change', function() {
    alert("Hello");
}, false);
