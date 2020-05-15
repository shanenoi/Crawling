var header = "\t\t\t";
var paragraph_splitting_key = "\t\t\t\t\t\t";
var list = document.getElementsByClassName("zxU94d gws-plugins-horizon-jobs__tl-lvc")[0];
var post = {
    name: "BjJfJf PUpOsf",
    content: "HBvzbc"
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function get_element(tag_class_name) {
    return document.getElementsByClassName(tag_class_name);
}

function scroll_down(element) {
    element.scrollTo(0,element.scrollHeight);
}

function export_string(content) {
    var encodedUri = encodeURI(
        "data:text/csv;charset=utf-8," +
        content
    );
    window.open(encodedUri);
}

async function main() {
    while (true) {
        recu = String(document.documentElement.innerText);
        for (var i=0; i<50; i++) {
            scroll_down(list);
            await sleep(300x);
        }
        if (recu == String(document.documentElement.innerText)) {
            break;
        }
    }
    n = get_element(post.name);
    c = get_element(post.content);
    data = "";
    for (var i=0; i<n.length; i++) {
        data += (
            n[i].innerText + header +
            c[i].innerText + paragraph_splitting_key
        );
    }
    export_string(data);
}
main();
