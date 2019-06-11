//预校验注册表单数据

$(document).ready(function () {
    // alert("haha")
    //用户名有效性
    var input_accunt = document.getElementById("accunt");

    input_accunt.addEventListener("blur", function(){
        instr = this.value;
        if (instr.length < 6 || instr.length > 12){
            accunterr.style.display = "block"
            return
        }

        $.post("/App/CheckUserId/", {"userid":instr}, function(data){
            if (data.status == "error"){

                checkerr.style.display = "block"
            }

        })
    },false)
});

