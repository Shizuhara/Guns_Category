// 検索結果0件の場合, 表題を削除, 文言を変更
var hidden_figure = document.querySelectorAll('#result_table th')
var replacement_txt = document.getElementById('example_txt')
for(var hidden_th of hidden_figure) {
    console.log(document.getElementById('result_numbers').innerHTML)
    if (document.getElementById('result_numbers').innerHTML == '0件') {
        hidden_th.hidden = true;
        var zero_hidden = document.getElementById('example_txt')
        zero_hidden.innerHTML = '結果が見つかりませんでした. 条件を変更して検索してください. '
    }
}

// addEventListener
// チェックボックスにチェックが入る
// チェックしたタグをトグルで追記
var change_ele = document.getElementsByClassName('deploy_hantei');
console.log('change_ele: ' + change_ele);
for(var hoge of change_ele){
    hi = hoge.firstChild;
    console.log('hoge: ' + hi);
    hoge.addEventListener('change', function() {
        hi.classList.toggle('hidden_hantei')
    }, false);
}

// チェックを他要素につける
function simple_tree( textid, ischecked ){
    var genre = document.getElementsByClassName(textid);
    if( ischecked == true ) {
        for(var ele of genre) {
            others_checked_true(ele);
            fieldset_dispaly_inline(ele.parentElement);
        }
    }
    else{
        for(var ele of genre) {
            others_checked_flase(ele);
        }
    }
}

// 親をクリックした時
function deploy_tree( textid, ischecked ){
    var dispaly_hantei = document.getElementById(textid);
    if( ischecked == true ) {
        fieldset_dispaly_inline(dispaly_hantei)
    }
    else {
        fieldset_dispaly_none(dispaly_hantei)
    }
}
// combをクリックした時
function comb_tree( textid, ischecked ){
    var genre = document.getElementsByClassName(textid);
    if( ischecked == true ) {
        var cnt = 0
        // fieldset内部へ
        for(var ele of genre) {
            // 連動してチェックをつける
            others_checked_true(ele);
            // 連動してfieldset表示(無駄な回数やるけど無問題)
            fieldset_dispaly_inline(ele.parentElement);
            // 連動して関係する親のチェックボックスもチェック
            cnt += 1
            console.log('カウンタ: ' + cnt)
            console.log('element: ' + document.getElementById(ele.name).firstElementChild.textContent)
            others_checked_true(document.getElementById(ele.name).firstElementChild)
        }
    }
    else{
        for(var ele of genre) {
            // 連動して他要素のチェックを外す
            others_checked_flase(ele)
            // 他combがクリックされている時消しすぎるので干渉分を補填
            comb_checked_hantei()
            // fieldsetの中身が空の場合は閉じる
            depoy_false(ele)
        }
    }
}

// 他要素もtrue
function others_checked_true(elements){
    elements.checked = true;
}
// 他要素もflase
function others_checked_flase(elements){
    elements.checked = false;
}
// fieldset表示
function fieldset_dispaly_inline(elements){
    elements.style.display = "inline-block";
}
// fieldset非表示
function fieldset_dispaly_none(elements){
    elements.style.display = "none";
}
// 指定した要素を全て取得
function depoy_false(checked_ele){
    var elements = checked_ele.parentElement.childNodes
    var cnt = 0
    // console.log(checked_ele)
    // console.log(document.getElementById(elements))
    // console.log(elements)
    for (var ele of elements){
        // console.log(ele.checked)
        if (ele.checked == true) {
            cnt += 1
        }
    }
    // console.log(cnt)
    if (cnt == 0) {
        // 親要素を隠す
        fieldset_dispaly_none(checked_ele.parentElement);
        // 親要素のチェックを外す
        checked_ele.parentElement.parentElement.firstElementChild.checked = false;
    }
}
// 他コンビのチェック状況(コンビのチェックを外した時に実行)
function comb_checked_hantei(){
    var comb_elements = document.getElementsByName('Comb');
    for (var comb_element of comb_elements){
        // combのチェックを外した時に動くif文なので他のcombを取得可能
        // 他のcombにチェックが入っているか
        if(comb_element.checked == true){
            var checked_class = document.getElementsByClassName(comb_element.value);
            for(var checked_ele of checked_class){
                // 連動して他要素をチェック
                checked_ele.checked = true;
                // checked_ele.parentElement.style.display = "inline-block";
                // 親にチェックを入れる
                checked_ele.parentElement.parentElement.firstElementChild.checked = true;
                console.log(checked_ele.parentElement.parentElement.firstChild.value);
            }
        }
    }
}
// class はドット, id はハッシュ