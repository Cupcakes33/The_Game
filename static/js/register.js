const usernameCheck = $('.username-check');
const nicknameCheck = $('.nickname-check');
const passwordCheck = $('.password-check');
const repeatCheck = $('.repeat-check');


const registerId = $('#register-id')
const registerNickname = $('#register-nickname')
const registerPw = $('#register-pw')
const checkingPw = $('#checking-pw')
const registerSubmit = $('#register-submit')

const duplicateId = $('.duplicate-id')
const duplicateNickname = $('.duplicate-nickname')

const USERNAME_REG = /^(?=.*[a-z0-9])[a-z0-9]{6,16}$/
// 닉네임 정규식 toLowerCase() 유저네임은 toLowerCase() 로변환하여 db에 저장.
const PASSWORD_REG = /^(?=.*[0-9])(?=.*[a-zA-Z])[a-zA-Z0-9!@#$%^&*()._-]{6,16}$/
// 비밀번호 정규식 6~16 적어도 하나이상의 숫자, 문자. 특수문자 허용
const NICKNAME_REG = /^(?=.*[a-z0-9가-힣])[a-z0-9가-힣]{2,16}$/
// 닉네임 정규식 2~16 영어, 숫자, 한글로 구성. 한글 초성 및 모음은 허가하지 않음


const submitButtonActive = () => {
    if (usernameCheck.hasClass('isDone') && nicknameCheck.hasClass('isDone') &&
        passwordCheck.hasClass('isDone') && repeatCheck.hasClass('isDone') &&
        duplicateId.hasClass('true') && duplicateNickname.hasClass('true')) {
        registerSubmit.addClass('active')
        registerSubmit.attr('disabled', false)
    } else {
        registerSubmit.removeClass('active')
        registerSubmit.attr('disabled', true)
    }
}

registerId.on('input',()=>{
    duplicateId.removeClass('true').removeClass('false')
    submitButtonActive()
})
registerNickname.on('input',()=>{
    duplicateNickname.removeClass('true').removeClass('false')
    submitButtonActive()
})


registerId.focusout(() => {

    let username = registerId.val();
    if (username.length === 0) {
        usernameCheck.show().text('Please input Username').removeClass('isDone')
    } else if (username.length < 6) {
        usernameCheck.show().text('Username at least 6 characters').removeClass('isDone')
    } else if (!USERNAME_REG.test(username)) {
        usernameCheck.show().text('Invalid Username').removeClass('isDone')
    } else {
        usernameCheck.hide().addClass('isDone');
    }
    submitButtonActive()
})

registerNickname.focusout(() => {

    let nickname = registerNickname.val();
    if (nickname.length === 0) {
        nicknameCheck.show().text('Please input Nickname').removeClass('isDone')
    } else if (nickname.length < 2) {
        nicknameCheck.show().nicknameCheck.text('is too short').removeClass('isDone')
    } else if (!NICKNAME_REG.test(nickname)) {
        nicknameCheck.show().nicknameCheck.text('invalid Nickname !').removeClass('isDone')
    } else {
        nicknameCheck.hide().addClass('isDone')
    }
    submitButtonActive()
})

registerPw.focusout(() => {

    let passwordValue = registerPw.val()
    if (passwordValue === '') {
        passwordCheck.show().text('Please input Password').removeClass('isDone')
    } else if (!PASSWORD_REG.test(passwordValue)) {
        passwordCheck.show().text('Al least 6 characters, num and letters').removeClass('isDone')
    } else {
        passwordCheck.hide().addClass('isDone')
    }
    submitButtonActive()
})

checkingPw.focusout(() => {

    let passwordValue = registerPw.val()
    let repeatValue = checkingPw.val()
    if (repeatValue !== passwordValue) {
        repeatCheck.show().text('Passwords do not match').removeClass('isDone')
    } else {
        repeatCheck.hide().addClass('isDone')
    }
    submitButtonActive()
})

// 회원가입 API

const postRegister = (id, pw, nick) => {
    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {
            id_give: id,
            pw_give: pw,
            nickname_give: nick
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/login'
            } else {
                alert(response['msg'])
            }
        }
    })
}

registerSubmit.click((e) => {
    e.preventDefault()
    let id = registerId.val().toLowerCase()
    let nickname = registerNickname.val()
    let pw = registerPw.val()

    if (duplicateId.hasClass(true) && duplicateNickname.hasClass(true)) {
        postRegister(id, pw, nickname)
    } else {
    }

})

duplicateId.click((e) => {
    e.preventDefault();
    let id = registerId.val().toLowerCase();
    console.log(id)
    if(usernameCheck.hasClass('isDone')){
        $.ajax({
        type: 'GET',
        url: '/api/duplicate/id',
        data: { id_give: id },
        success: (res)=>{
            const result = res.result;
            console.log(result)
            if(result === 'not_duplicate'){
              duplicateId.removeClass('false').addClass('true')
            } else {
                duplicateId.removeClass('true').addClass('false')
            }
        }
    })
    }else {

    }

})

duplicateNickname.click((e) => {
    e.preventDefault();
    let nickname = registerNickname.val()
    console.log(nickname)
    if(nicknameCheck.hasClass('isDone')){
        $.ajax({
        type: 'GET',
        url: '/api/duplicate/nickname',
        data: { nickname_give: nickname },
        success: (res)=>{
            const result = res.result;
            if(result === 'not_duplicate'){
              duplicateNickname.removeClass('false').addClass('true')
            } else {
                duplicateNickname.removeClass('true').addClass('false')
            }
        }
    })
    }

})




