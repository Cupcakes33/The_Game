const screens = document.querySelectorAll('.screen');
const choose_insect_btns = document.querySelectorAll('.choose-insect-btn');
const start_btn = document.getElementById('start-btn')
const game_container = document.getElementById('game-container')
const timeEl = document.getElementById('time')
const scoreEl = document.getElementById('score')

let seconds = 0
let score = 0
let selected_insect = {}

document.oncontextmenu = function(){return false;}

$(document).ready(function () {
    $("#screen1").hide()
    $("#screen2").show()
    $("#game-container").hide()
})

$("#start-btn").click(function () {
    allhide()
    $("#screen2").fadeIn(600)
})

function allhide() {
    $("#screen1").fadeOut(300)
    $("#screen2").fadeOut(300)
    $("#game-container").fadeOut(300)
}

choose_insect_btns.forEach(btn => {
    btn.addEventListener('click', () => {
        const img = btn.querySelector('img')
        const src = img.getAttribute('src')
        const alt = img.getAttribute('alt')
        selected_insect = {src, alt}
        allhide()
        $("#game-container").fadeIn(600)
        setTimeout(createInsect, 1000)
        increaseTime()
    })
})

function increaseTime() {
    let timer = setInterval(function () {
        let m = Math.floor(seconds / 60)
        let s = seconds % 60
        m = m < 10 ? `0${m}` : m
        s = s < 10 ? `0${s}` : s
        timeEl.innerHTML = `Time: ${m}:${s}`
        seconds++
        if (m == 1) {
            clearInterval(timer)
            save_order()
        }
    }, 1000)
}

function createInsect() {
    const insect = document.createElement('div')
    insect.classList.add('insect')
    const {x, y} = getRandomLocation()
    insect.style.top = `${y}px`
    insect.style.left = `${x}px`
    insect.innerHTML = `<img src="${selected_insect.src}" alt="${selected_insect.alt}" style="transform: rotate(${Math.random() * 360}deg)"/>`
    insect.addEventListener('click', catchInsect)

    game_container.appendChild(insect)
}

function getRandomLocation() {
    const width = window.innerWidth
    const height = window.innerHeight
    const x = Math.random() * (width - 200) + 100
    const y = Math.random() * (height - 200) + 100
    return {x, y}
}

function catchInsect() {
    increaseScore()
    this.classList.add('caught')
    setTimeout(() => this.remove(), 2000)
    addInsects()
}

function addInsects() {
    if (seconds <= 59) {
        setTimeout(createInsect, 1000)
        setTimeout(createInsect, 1500)
    }
}

function increaseScore() {
    if (seconds <= 59) {
        score++
    }
    scoreEl.innerHTML = `Score: ${score}`
}

function save_order() {
    $.ajax({
        type: 'POST',
        url: '/game',
        data: {score_give: score},
        success: function (response) {
            console.log(response['msg'])
            window.location.href = './rank/game_end'
        }
    });
}



///////////////////////////철컹 철컹 철컹 철컹 경찰청!!!!!//////////////////////////////////
///////////////////////////밑에거 주석만 풀면 됩니다!!!////////////////////////////////////

// !function() {
//   function detectDevTool(allow) {
//     if(isNaN(+allow)) allow = 100;
//     var start = +new Date();
//     debugger;
//     var end = +new Date();
//     if(isNaN(start) || isNaN(end) || end - start > allow) {
//       // 개발자 도구가 open 된것을 감지했을때 실행할 코드 삽입
//       alert('개발자 도구가 감지되었습니다!');
//       document.location.href="https://www.police.go.kr/index.do"
//     }
//   }
//   if(window.attachEvent) {
//     if (document.readyState === "complete" || document.readyState === "interactive") {
//         detectDevTool();
//       window.attachEvent('onresize', detectDevTool);
//       window.attachEvent('onmousemove', detectDevTool);
//       window.attachEvent('onfocus', detectDevTool);
//       window.attachEvent('onblur', detectDevTool);
//     } else {
//         setTimeout(argument.callee, 0);
//     }
//   } else {
//     window.addEventListener('load', detectDevTool);
//     window.addEventListener('resize', detectDevTool);
//     window.addEventListener('mousemove', detectDevTool);
//     window.addEventListener('focus', detectDevTool);
//     window.addEventListener('blur', detectDevTool);
//   }
// }();