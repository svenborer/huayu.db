function color_code_hanzi(hanzi_id, pinyin_numerical) {
    var special_chars = ['…','／','（','）']
    special_chars.forEach(function(c){
        pinyin_numerical = pinyin_numerical.split(c).join(c+'5')
    })
    tone_list = pinyin_numerical.match(/\d+/g);
    hanzi = $(hanzi_id).text()
    $(hanzi_id).text("")
    i = 0
    tone_list.forEach(function(t){
        switch (t) {
            case "1":
                color = 'red-text'
                break;
            case "2":
                color = 'green-text'
                break;
            case "3":
                color = 'indigo-text'
                break;
            case "4":
                color = 'purple-text'
                break;
            case "5":
                color = ''
                break;
            default:
                break;
        }
        $('#hanzi').append("<span class=\""+color+"\">"+hanzi[i++]+"<span>")
    })
}

function color_code_examples(hanzi_id, example_class) {
    var hanzi = $(hanzi_id).text();
    var hanzi_list = hanzi.split('／');

    $(example_class).each(function () {
        e = $(this)
        hanzi_list.forEach(function (item) {
            if (item.match(/….*/)) {
                item.split('…').forEach(function (item) {
                    var re = new RegExp(item,"g");
                    example = e.html().replace(re, "<span class=\"highlight\">" + item + "</span>")
                    e.html(example);
                })
            } else {
                var re = new RegExp(item,"g");
                example = e.html().replace(re, "<span class=\"highlight\">" + item + "</span>")
                e.html(example);
            }
        })
    });
}