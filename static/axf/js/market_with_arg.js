$(document).ready(function () {
    var alltypebtn = document.getElementById("alltypebtn")
    var showsortbtn = document.getElementById("showsortbtn")

    var typediv = document.getElementById("typediv")
    var sortdiv = document.getElementById("sortdiv")

    typediv.style.display = "none"
    sortdiv.style.display = "none"


    alltypebtn.addEventListener("click", function () {
        typediv.style.display = "block"
        sortdiv.style.display = "none"
    }, false)
    showsortbtn.addEventListener("click", function () {
        typediv.style.display = "none"
        sortdiv.style.display = "block"
    }, false)
    typediv.addEventListener("click", function () {
        typediv.style.display = "none"
    }, false)
    sortdiv.addEventListener("click", function () {
        sortdiv.style.display = "none"
    }, false);
    //yellowSlide


    $('.aside').click(function () {
        // alert("haha");
        console.log("pos");
        $('.yellowSlide').style.display = "block";

    });
    //修改购物车

    var add_shopping = document.getElementsByClassName("addShopping");
    // add_shopping.click(function () {
    //     console.log('点到我了');
    //     var sum1 = this.prev().text();
    //     sum1 = sum1 + 1;
    //     this.prev().text(sum1)
    // });
    // for(var i=0; i<=add_shopping.length; i++){
    //     var add_shop = add_shopping[i];
    //
    //     add_shop.addEventListener("click", function () {
    //
    //     console.log('点到我了');
    //     console.log(this);
    //     // console.log(this.prev());
    //     // this.style.display = 'none';
    //     var sum1 = $(this).prev().text();
    //     sum1 = sum1 + 1;
    //     this.prev().text(sum1)
    //     },false)
    // }

    console.log("tou")
    var nums = document.getElementsByClassName("num")
    for (var k; k < nums.length; k++) {
        var num = nums[k];
        var pid = num.getAttribute("id")
        $.post("/App/ChangeCartNum/", {'pid': pid}, function (data) {
            console.log(data);
            $("#" + pid).text(data["goods_nums"])
        })
    }


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
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function () {
            pid = this.getAttribute("pID")
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


})