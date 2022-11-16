// login Form control

const loginId = $('#login-id')
const loginPw = $('#login-pw')
const loginSubmit = $('#login-submit')



const isInputCheck = () => {
    if(loginId.val() !== '' && loginPw.val() !== '' && loginId.val().length > 5 && loginPw.val().length > 5){
        loginSubmit.attr('disabled',false)
        loginSubmit.addClass('active')
    }else {
        loginSubmit.attr('disabled',true)
        loginSubmit.removeClass('active')
    }
}

loginId.on('input',isInputCheck)
loginPw.on('input',isInputCheck)

const signin = () => {
    $.ajax({
        type: "POST",
        url:'/api/login',
        data: {
            login_id: loginId.val(),
            login_pw: loginPw.val(),
        },
        success: function (res) {
            if(res['result']==='success'){
                $.cookie('mytoken', res['token'])
                alert('로그인 완료 !')
                window.location.href ='./'
            } else {
                alert(res['msg'])
            }
        }
    })
}

loginSubmit.click((e)=>{
    e.preventDefault()
    signin()
})

