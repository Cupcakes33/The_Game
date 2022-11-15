// {% if msg %}
//     alert("{{ msg }}")
// {% endif %}

const login = () => {

    $.ajax({
        type: 'POST',
        url: '/api/login',
        data: {login_id: $('#id').val(), login_pw: $('#pw').val()},
        success: (response) => {

            if (response['result'] === 'success') {
                $.cookie('mytoken', response['token'])

                alert('로그인 완료');
            } else {

                alert(response['msg'])
            }
        }
    })

}


