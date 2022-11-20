//const start_btn = document.getElementById('start-btn')
//const Rank_btn = document.getElementById('Rank-btn')
//start_btn.addEventListener('click', () => screens[0].classList.add('up'))
//Rank_btn.addEventListener('click', () => Rank_page_url)
const insert_btn = document.getElementById('comment-insert-btn')
const reportbutton = document.querySelector('#report-button')


insert_btn.addEventListener('click', () => {
    if ($("#comment-input").val() !== '') {
        save_comment()
    }
})

$(document).ready(function () {
    show_comment();
});

function logout() {
    $.removeCookie('mytoken');
    window.location.href = './login'
}


function save_comment() {
    // let user_nickname = $('#user_nickname').val()
    let comment = $('.comments-form-input').val().replace(/\n/g, "<br>")
    $.ajax({
        type: 'POST',
        url: '/user',
        data: {comment: comment},
        success: function () {
            window.location.reload()
        }
    })
}

function show_comment() {
    $.ajax({
        type: "GET",
        url: "/user",
        data: {},
        success: function (response) {


            let rows = response['comments'].sort(function (a, b) {
                return new Date(b.date) - new Date(a.date);
            })


            for (let i = 0; i < rows.length; i++) {

                let comment = rows[i]['comment']
                let date = rows[i]['date']
                let nick = rows[i]['user_nickname']

                let temp_html = `
                        <div class="comment-list">
                        <div>
                            <span class="comment-nickname-text">${nick}</span>
                            <span class="comment-time-text">${date}</span>
                            <span id="report-button""> 신고하기 </span>
                            </div>
                            <div class="comment-content">${comment}</div>
                        </div>
                        `

                $('.comment-box').append(temp_html)
            }
        },
    })
}


$('.comments-form-input').on('keydown', (e) => {
    if (e.keyCode == 13 && !e.shiftKey) {
        e.preventDefault();
        save_comment()
        return true;
    }
})

document.addEventListener('click', function (e) {
    if (e.target && e.target.id == 'report-button') {
        let date = e.target.parentElement.children[1].innerText
        $.ajax({
            type: "POST",
            url: "api/report",
            data: { date:date },
            success: function (response) {
                alert(response.msg)
            }
        })
    }
});