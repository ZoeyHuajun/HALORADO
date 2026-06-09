function bindEmailCodeClick(){
    //bind click
    $("#captcha-btn").click(function(event){
        //prevent submit all of the date
        event.preventDefault();

        let that = $(this); //jquery format

        // 1. get enter email
        let email = $("#reg-email").val();
        //email correct format
        let emailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
        if(!emailReg.test(email)){
            alert("Please enter a valid Email.");
            return;
        }

        // 2. cancel click function before countdown
        that.off('click');

        // 3. countdown 6s
        let countdown = 6;
        that.text(countdown+"s");
        let timer = setInterval(function(){
            countdown -= 1;
            that.text(countdown+"s");
            if(countdown <= 0){
                that.text("Get varification code");
                clearInterval(timer);
                // bind click again
                bindEmailCodeClick();
            }
        }, 1000);

        // 4. ajax
        $.get({
            url: "/email/code",
            data: {"email": email},
            success: function (result){
                console.log(result);
            }
        });
    });
}



// 整个网页加载完成后
$(function(){
    bindEmailCodeClick();
    //bindRegisterEvent();
})