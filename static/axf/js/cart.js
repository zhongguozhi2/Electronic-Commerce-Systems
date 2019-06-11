$(function () {
    // 修改购物车
    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    for (var i = 0; i < addShoppings.length; i++) {
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function () {
            pid = this.getAttribute("pID")
            console.log("diandaowole")
            $.post("/App/ChangeCart/0/", {"pID": pid}, function (data) {
                console.log("faguoqule")
                if (data.status == 200) {
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.nums
                } else {
                    if (data.status == 600) {
                        window.location.href = "http://127.0.0.1:8000/App/login/"
                    }
                }
            })
        })
    }


    for (var i = 0; i < subShoppings.length; i++) {
        subShopping = subShoppings[i];
        subShopping.addEventListener("click", function () {
            pid = this.getAttribute("pID");
            $.post("/App/ChangeCart/1/", {"pID": pid}, function (data) {
                if (data.status == 200) {
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.nums
                } else {
                    if (data.status == 600) {
                        window.location.href = "http://127.0.0.1:8000/App/login/"
                    }
                }
            })
        })
    }
    var confirm = document.getElementsByClassName("confirm");

    for (var t = 0; t < confirm.length; t++) {
        // var cartid = confirm[t].find("span").getAttribute("cartid");
        // console.log(confirm[t]);
        var button1 = confirm[t];


        var confirm1 = $(button1).find("span")[0];
        // console.log($(button1).find("span"));
        // console.log(confirm1);
        confirm1.addEventListener("click", function () {
            var cartid = $(this)[0].getAttribute("cartid");
            // console.log($(this)[0]);
            // console.log(cartid);
            // console.log('aaaaaaaaaaaaaaaaaa')
            $.post("/App/ChangeStatus/", {'cartid': cartid}, function (data) {
                console.log(data);
                if (data["is_select"]) {
                    // console.log($(this));
                    // console.log($("span.cartid"))
                    // console.log($("span[cartid="+cartid+"]"))
                    $("span[cartid=" + cartid + "]").find("span").text("√")

                } else {
                    $("span[cartid=" + cartid + "]").find("span").text("")
                }
                if (data["if_all_select"] === true) {

                    $(".all_select").find("span").find("span").text("√")

                } else {
                    $(".all_select").find("span").find("span").text("")

                }
            })
        })
    }

    var $all_select_btn = $(".all_select").find("span");
    $all_select_btn.click(function () {
        console.log($all_select_btn.find("span").text());
        if ($all_select_btn.find("span").text() === "√") {
            var state = 1
        }

        if ($all_select_btn.find("span").text() === "") {
            state = 0
        }
        console.log(state+"hahaahahah")
        $.getJSON('/App/ChangeAllStatus/', {'state': state}, function (data) {
            console.log('haahah')
            if(data['status']===200){
                if (state===1) {
                    console.log($(this))
                    $all_select_btn.find("span").text("")
                    $(".confirm").find("span").find("span").text("")

                } else {
                    $all_select_btn.find("span").text("√");
                    $(".confirm").find("span").find("span").text("√")
                }
            }

        })

    })

});