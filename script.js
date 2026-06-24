
function launchConfetti() {
    const canvas = document.getElementById("confetti-canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const pieces = [];
    const colors = ["#f44336","#e91e63","#9c27b0","#3f51b5","#2196f3","#00bcd4","#4caf50","#ffeb3b","#ff9800","#ff5722"];
    for (let i = 0; i < 200; i++) {
        pieces.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height - canvas.height,
            w: Math.random() * 10 + 5,
            h: Math.random() * 6 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            rot: Math.random() * Math.PI * 2,
            rotSpeed: (Math.random() - 0.5) * 0.15,
            vy: Math.random() * 3 + 2,
            vx: (Math.random() - 0.5) * 2,
        });
    }
    let frame;
    let elapsed = 0;
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let allGone = true;
        for (const p of pieces) {
            p.y += p.vy;
            p.x += p.vx;
            p.rot += p.rotSpeed;
            if (p.y < canvas.height + 20) allGone = false;
            ctx.save();
            ctx.translate(p.x + p.w / 2, p.y + p.h / 2);
            ctx.rotate(p.rot);
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
            ctx.restore();
        }
        elapsed++;
        if (!allGone && elapsed < 400) {
            frame = requestAnimationFrame(draw);
        } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }
    draw();
}

function glitchTitle() {
    const titleEl = document.querySelector(".title");
    const original = "Grow a Flower";
    const glitchChar = "\uFFFD";
    setInterval(() => {
        let chars = original.split("");
        const numGlitches = Math.floor(Math.random() * 5) + 1;
        for (let i = 0; i < numGlitches; i++) {
            const idx = Math.floor(Math.random() * chars.length);
            if (chars[idx] !== " ") chars[idx] = glitchChar;
        }
        titleEl.textContent = chars.join("");
        setTimeout(() => { titleEl.textContent = original; }, 80);
    }, 300);
}
function glitchHeading() {
    const titleEl = document.querySelector("#heading");
    const original = "About Grow a Plant.CO (Actual)";
    const glitchChar = "\uFFFD";
    setInterval(() => {
        let chars = original.split("");
        const numGlitches = Math.floor(Math.random() * 5) + 1;
        for (let i = 0; i < numGlitches; i++) {
            const idx = Math.floor(Math.random() * chars.length);
            if (chars[idx] !== " ") chars[idx] = glitchChar;
        }
        titleEl.textContent = chars.join("");
        setTimeout(() => { titleEl.textContent = original; }, 80);
    }, 300);
}


function toggleMusic() {
    const musicAudio = document.getElementById("music-audio");
    const musicBtn = document.getElementById("music-btn");
    if (musicAudio.paused) {
        musicAudio.play();
        musicBtn.textContent = "\u{1F50A}";
    } else {
        musicAudio.pause();
        musicBtn.textContent = "\u{1F507}";
    }
}
function validate() {
    const aboutMake = document.getElementById('about-make');
    const passwordInput = document.querySelector('.password');
    const resultDiv = document.getElementById('result');
    const submitButton = document.querySelector('.submit');
    const body = document.getElementById('background');
    const aboutUs = document.getElementById('about-us');
    const aboutMission = document.getElementById('about-mission');
    const appleOpinion = document.getElementById('apple-opinion');
    const governmentOpinion = document.getElementById('government-opinion');
    const bloomingFlowerOpinion = document.getElementById('blooming-flower-opinion');
    const password = passwordInput.value;

    if (password === 'blooming flower') {
        alert('Access granted');
        glitchHeading();
        const darkMusicAudio = document.getElementById("dark-music");
        submitButton.style.display = 'none';
        passwordInput.style.display = 'none';
        darkMusicAudio.volume = 0.5;
        try{ darkMusicAudio.play(); }catch(e){}
        document.body.classList.add('lore-mode');
        passwordInput.value = '';
        aboutMake.innerText = 'The truth is that we were not the creators of Grow a Flower in fact the person who did it is completely unknown, and we think that it had no creator at all and is an entity.';
        aboutUs.innerText = 'In reality we are a group of researchers and government officials studying the Grow a Flower anomalies and its connected real-world entity.';
        aboutMission.innerText = 'Our mission is to uncover the infinite mysteries surrounding Grow a Flower.';
        appleOpinion.innerText = 'A: We think that the shutdown was the necessary choice because of the experiment outbreaks and their disloyal behavior from the people in it. We also think this because of their sloppy thing they called "covering it up", but it is still sad to see another government test facility shutdown.';
        governmentOpinion.innerText = 'A: We obviously are the government and just like applePicker.CO, we are the highest level officials in the government, responsible for overseeing and regulating activities related to Grow a Flower and similar entities.';
        bloomingFlowerOpinion.innerText = 'A: Yes, we are testing on the "Blooming Flower" as it actually names the final phase of Grow a Flower, and once that stage is reached by a user the real-life counterpart in the form of vines grows a new flower.';
        resultDiv.innerHTML = 
        '<h3 class="header">Experiments and Findings</h3>' +
        '<h4 class="header">Findings</h4>' +
        '<p class="main-text"> Grow a Flower\'s counterpart in the real world is in the form of vines, and when sampled it shows it has plant tissue even though when met with a vegetarian or an organism that wants to destroy it. The vines will slash onto the organism and slowly suck the nutrients from them.</p>' +
        '<p class="main-text"> These vines not only do that, but also make new flowers when users reach the "Blooming Flower" stage. Of course the flowers are not the average flower as it grows in a day and gains unusual properties after 2 days of growing and will drop on the floor.</p>' +
        '<p class="main-text">The flower can change organisms once touched, smelled, or even talked about.</p>' +
        '<p class="main-text">Once a person has been changed it rarely is a beneficial change and when it is it only cures chronic neurodevelopmental disorders.</p>' +
        '<p class="main-text">Commonly it manipulates people\'s minds and makes them go outside almost always and makes them drink more water than they need. After a few days of that, the person slowly loses their sanity and they see spirals, patterns, and moving colors. Almost always it\'s so unbearable that the brain shuts down.</p>' +

        '<p class="main-text">Only a few documented times has the flower changed people structurally. At first the symptoms were average, but the brain doesn\'t shut down the 1st month nor the 2nd month until finally in the 3rd month they stand outside 24 hours and drink gallons of water before flowers slowly grow out of them and roots dig into the soil from them. It is unknown if they experience this while this phase is happening.</p>' +
        '<p class="main-text">Some people speculate that it\'s the vines\' way of finding hosts and stealing nutrients, but it is unknown why it spares a few people and even cures them of chronic neurodevelopmental disorders.</p>' +

        '<h4 class="header">Experiments</h4>' +
        '<p class="main-text">0001:<br> subject name: Ronald McDonald <br><br> subject touched flower and lost their extreme adhd symptoms.</p>' +
        '<p class="main-text">0055:<br> subject name: Jane Doe <br><br> day 1: subject heard about a flower and had been going outside almost always and drinking excessive amounts of water, showing early signs of sanity loss. day 4: subject continued the same behavior and began experiencing visual hallucinations similar to spirals and moving colors. day 7: subject\'s sanity further declined and they exhibited signs of extreme confusion and disorientation and later that day stopped breathing.</p>'+
        '<p class="main-text">b-01:<br> subject name: Zack Smith <br><br> day 1: subject going through normal consequences day 35: subject is still showing signs of life even though most patients would have succumbed by now. Observations continue day 65: patient is still alive, but has gone insane to the maximum extent observable and exhibits extreme behavioral changes. day 77: subject has drank gallons of water and is standing outside and looks to be growing roots from their feet and flowers that cover his entire body. He is also unresponsive but we\'re unable to tell if he\'s still alive in this phase</p>' +
        '<image src="music and images/Zack Smith.png" style="width:200px; height:200px; position:relative; left: 50%; transform:translateX(-50%);" alt="Experiment Image">' ;
        setTimeout(()=>{if(resultDiv.firstElementChild) resultDiv.firstElementChild.scrollIntoView({behavior:'smooth'});},120);
    } else {
        const errorAudio = document.getElementById("error");
        errorAudio.play();
        resultDiv.innerHTML = '<h4>Unauthorized: Incorrect password.</h4>';
    }
}