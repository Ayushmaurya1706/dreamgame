import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where <script> begins (after all HTML body)
script_start = content.index('<script>')
# Keep everything before the script tag
before = content[:script_start]

new_script = """<script>
    // GLOBAL ERROR DISPLAY
    window.onerror = function(msg, src, line, col, err) {
        var d = document.createElement('div');
        d.style.cssText = 'position:fixed;top:0;left:0;width:100%;background:rgba(200,0,0,0.97);color:#fff;z-index:999999;padding:20px;font-family:monospace;font-size:13px;white-space:pre-wrap;box-sizing:border-box;';
        d.innerText = 'JS ERROR: ' + msg + '\\nLine: ' + line + ':' + col + '\\n' + (err ? err.stack : '');
        document.body.appendChild(d);
        return false;
    };

    // TRAILER MODAL
    var currentSlide = 0;
    var slides = [
        { src: 'trailer_1.png', cap: 'Frame 1: Kael witnesses the destruction of the Kurogane forge.' },
        { src: 'trailer_2.png', cap: 'Frame 2: Face-off with General Ryu on the Sky Bridge.' },
        { src: 'trailer_3.png', cap: 'Frame 3: The Choice. Will you use the Cursed Shadow Blade?' }
    ];
    function openTrailer()  { document.getElementById('trailerModal').style.display = 'block'; }
    function closeTrailer() { document.getElementById('trailerModal').style.display = 'none'; }
    function changeSlide(n) {
        currentSlide = (currentSlide + n + slides.length) % slides.length;
        var img = document.getElementById('trailerImg');
        img.style.opacity = '0';
        setTimeout(function() {
            img.src = slides[currentSlide].src;
            img.onload = function() { img.style.opacity = '1'; };
        }, 150);
        document.getElementById('trailerCap').innerText = slides[currentSlide].cap;
    }

    // CHARACTER MODAL - ANIMATION 2 (frames 183-240, 58 frames, all exist)
    var charCanvas = document.getElementById('char-canvas');
    var charCtx = charCanvas.getContext('2d');
    var charImgSrcs = [];
    for (var ci = 183; ci <= 240; ci++) {
        charImgSrcs.push('Animation 2/ezgif-frame-' + ci + '.jpg');
    }
    var charImgs = [], charLoaded = 0, charReady = false;
    var charModalOpen = false, charFrameIdx = 0, charLastTime = 0;
    var CHAR_INTERVAL = 1000 / 24;

    function preloadCharFrames() {
        charImgSrcs.forEach(function(src) {
            var img = new Image();
            img.onload = img.onerror = function() {
                charLoaded++;
                if (charLoaded === charImgSrcs.length) charReady = true;
            };
            img.src = src;
            charImgs.push(img);
        });
    }

    function resizeCharCanvas() {
        if (!charCanvas || !charCanvas.parentElement) return;
        var r = charCanvas.parentElement.getBoundingClientRect();
        if (r.width > 0 && r.height > 0) {
            charCanvas.width = r.width;
            charCanvas.height = r.height;
        }
    }

    function drawCharFrame(idx) {
        var w = charCanvas.width, h = charCanvas.height;
        charCtx.clearRect(0, 0, w, h);
        if (!charReady || !charImgs.length) {
            charCtx.fillStyle = '#000'; charCtx.fillRect(0, 0, w, h);
            charCtx.fillStyle = '#00f3ff'; charCtx.font = '14px monospace';
            charCtx.textAlign = 'center';
            charCtx.fillText('LOADING WARRIOR...', w / 2, h / 2);
            return;
        }
        var img = charImgs[idx % charImgs.length];
        if (!img || img.width === 0) return;
        var ir = img.width / img.height, cr = w / h;
        var dw, dh, dx, dy;
        if (cr > ir) { dw = w; dh = w / ir; dx = 0; dy = (h - dh) / 2; }
        else          { dw = h * ir; dh = h; dx = (w - dw) / 2; dy = 0; }
        charCtx.drawImage(img, dx, dy, dw, dh);
        charCtx.strokeStyle = 'rgba(0,243,255,0.04)'; charCtx.lineWidth = 1;
        for (var y = 0; y < h; y += 4) {
            charCtx.beginPath(); charCtx.moveTo(0, y); charCtx.lineTo(w, y); charCtx.stroke();
        }
    }

    function renderCharLoop(ts) {
        if (!charModalOpen) return;
        requestAnimationFrame(renderCharLoop);
        var el = ts - charLastTime;
        if (el < CHAR_INTERVAL) return;
        charLastTime = ts - (el % CHAR_INTERVAL);
        drawCharFrame(charFrameIdx);
        if (charReady) charFrameIdx = (charFrameIdx + 1) % charImgs.length;
    }

    function openCharModal() {
        var m = document.getElementById('charModal');
        m.style.display = 'flex';
        charModalOpen = true; charFrameIdx = 0; charLastTime = 0;
        requestAnimationFrame(function() {
            resizeCharCanvas();
            requestAnimationFrame(renderCharLoop);
        });
    }

    function closeCharModal() {
        document.getElementById('charModal').style.display = 'none';
        charModalOpen = false;
    }

    function launchGameSim() {
        if (!document.getElementById('boot-style')) {
            var s = document.createElement('style'); s.id = 'boot-style';
            s.innerHTML = '@keyframes blink-caret{from,to{border-color:transparent}50%{border-color:#00f3ff}}';
            document.head.appendChild(s);
        }
        var ov = document.createElement('div');
        ov.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:#05050a;z-index:3000;display:flex;flex-direction:column;justify-content:center;align-items:center;font-family:monospace;color:#00f3ff;padding:40px;box-sizing:border-box;font-size:1rem;';
        var bc = document.createElement('div'); bc.style.cssText = 'max-width:600px;width:100%;';
        ov.appendChild(bc); document.body.appendChild(ov);
        var lines = [
            '>> INITIALIZING SHADOW BLADE SYSTEM...',
            '>> CONNECTING TO NEO-SAITAMA BATTLE-NET [PORT: 9811]...',
            '>> SECURING ENCRYPTED PROTOCOL... SUCCESS.',
            '>> RESOLVING CORE IDENTITY: "KAEL" [STATUS: betrayed_recon]...',
            '>> LINKING CURSED SHADOW BLADE HARDWARE ID... SYNCED.',
            '>> DOWNLOADING TACTICAL DATA: Kurogane Village [100%]...',
            '>> BYPASSING SHADOW CORE FIREWALL... COMPLETED.',
            '>> ENGAGING TACHYON DRIVE...',
            '>> SHADOW BLADE CLIENT LAUNCHED. WELCOME, KAEL.'
        ];
        var li = 0;
        function nextLine() {
            if (li >= lines.length) {
                setTimeout(function() {
                    ov.style.transition = 'opacity 0.6s'; ov.style.opacity = '0';
                    setTimeout(function() {
                        if (ov.parentNode) ov.parentNode.removeChild(ov);
                        closeCharModal();
                    }, 600);
                }, 1200);
                return;
            }
            var p = document.createElement('p');
            p.style.cssText = 'margin:8px 0;white-space:nowrap;overflow:hidden;border-right:2px solid #00f3ff;animation:blink-caret 0.75s step-end infinite;';
            bc.appendChild(p);
            var ci2 = 0, txt = lines[li];
            function typeChar() {
                if (ci2 < txt.length) { p.textContent += txt[ci2++]; setTimeout(typeChar, 14); }
                else { p.style.borderRight = 'none'; li++; setTimeout(nextLine, 110); }
            }
            typeChar();
        }
        nextLine();
    }

    // SCROLL REVEAL
    var revealObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                setTimeout(function() { entry.target.classList.add('visible'); }, entry.target.dataset.delay || 0);
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });

    // HERO CANVAS ANIMATION
    // Folder has frames 001-146. Load odd frames 001,003,...,145 = 73 frames (indices 0-72)
    // Idle: cycles 0-42 | Raise: 43-55 | Slash: 55-65 | Recover: 65-72
    var canvas = document.getElementById('hero-canvas');
    var ctx = canvas.getContext('2d');

    var framePaths = [];
    for (var fi = 1; fi <= 145; fi += 2) {
        var padded = ('00' + fi).slice(-3);
        framePaths.push('ezgif-394856e9406b723b-jpg/ezgif-frame-' + padded + '.jpg');
    }

    var images = [], isLoaded = false;

    var swordKF = {
        0:  { tip:{x:640,y:520}, base:{x:640,y:560} },
        35: { tip:{x:640,y:480}, base:{x:640,y:520} },
        43: { tip:{x:640,y:450}, base:{x:640,y:500} },
        48: { tip:{x:680,y:300}, base:{x:640,y:450} },
        55: { tip:{x:780,y:150}, base:{x:660,y:350} },
        57: { tip:{x:820,y:220}, base:{x:670,y:380} },
        59: { tip:{x:800,y:320}, base:{x:660,y:400} },
        61: { tip:{x:700,y:460}, base:{x:610,y:440} },
        63: { tip:{x:520,y:540}, base:{x:530,y:450} },
        65: { tip:{x:350,y:580}, base:{x:460,y:460} },
        67: { tip:{x:250,y:580}, base:{x:420,y:470} },
        69: { tip:{x:220,y:570}, base:{x:400,y:480} },
        72: { tip:{x:200,y:580}, base:{x:380,y:490} }
    };

    function getSwordCoords(idx) {
        var keys = Object.keys(swordKF).map(Number).sort(function(a,b){return a-b;});
        if (idx <= keys[0]) return swordKF[keys[0]];
        if (idx >= keys[keys.length-1]) return swordKF[keys[keys.length-1]];
        var pk = keys[0], nk = keys[1];
        for (var i = 0; i < keys.length-1; i++) {
            if (idx >= keys[i] && idx <= keys[i+1]) { pk = keys[i]; nk = keys[i+1]; break; }
        }
        var pv = swordKF[pk], nv = swordKF[nk], r = (idx-pk)/(nk-pk);
        return {
            tip:  { x: pv.tip.x  + (nv.tip.x  - pv.tip.x)  * r, y: pv.tip.y  + (nv.tip.y  - pv.tip.y)  * r },
            base: { x: pv.base.x + (nv.base.x - pv.base.x) * r, y: pv.base.y + (nv.base.y - pv.base.y) * r }
        };
    }

    var particles = [];
    function Particle(x, y, color) {
        this.x=x; this.y=y;
        this.vx=(Math.random()-0.5)*12; this.vy=(Math.random()-0.5)*12-3;
        this.size=Math.random()*4+2; this.life=1.0; this.decay=Math.random()*0.04+0.02;
        this.color=color;
    }
    Particle.prototype.update = function() { this.x+=this.vx; this.y+=this.vy; this.vy+=0.1; this.life-=this.decay; };
    Particle.prototype.draw = function(c) {
        c.fillStyle=this.color; c.globalAlpha=this.life; c.shadowColor=this.color; c.shadowBlur=10;
        c.beginPath(); c.arc(this.x,this.y,this.size,0,Math.PI*2); c.fill(); c.globalAlpha=1; c.shadowBlur=0;
    };

    var curFI = 0, tgtFI = 35, idleFC = 0;
    var LERP = 0.25;

    function resizeCanvas() {
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        if (isLoaded) drawFrame(images[Math.floor(curFI)], Math.floor(curFI));
    }
    window.addEventListener('resize', function() { resizeCanvas(); resizeCharCanvas(); });
    resizeCanvas();

    function drawFrame(img, idx) {
        if (!img || img.width === 0 || img.height === 0) return;
        var cw = canvas.width, ch = canvas.height;
        ctx.clearRect(0, 0, cw, ch);
        var ir = img.width/img.height, cr = cw/ch;
        var dw, dh, dx, dy;
        if (cr > ir) { dw=cw; dh=cw/ir; dx=0; dy=(ch-dh)/2; }
        else          { dw=ch*ir; dh=ch; dx=(cw-dw)/2; dy=0; }
        var scale = dw/1280;
        var sx=0, sy=0;
        if (idx>=57 && idx<=63) { sx=(Math.random()-0.5)*15*scale; sy=(Math.random()-0.5)*15*scale; }
        ctx.filter = (idx>=57 && idx<=63) ? 'blur(3px)' : 'none';
        ctx.drawImage(img, dx+sx, dy+sy, dw, dh);
        ctx.filter = 'none';
        var co = getSwordCoords(idx);
        var tip  = { x:dx+sx+co.tip.x*scale,  y:dy+sy+co.tip.y*scale  };
        var base = { x:dx+sx+co.base.x*scale, y:dy+sy+co.base.y*scale };
        // VFX: blade charge (43-55)
        if (idx>=43 && idx<=55) {
            var cp=(idx-43)/(55-43);
            ctx.shadowColor='#00f3ff'; ctx.shadowBlur=15+Math.sin(Date.now()/80)*8;
            ctx.strokeStyle='rgba(0,243,255,'+(0.4+cp*0.6)+')'; ctx.lineWidth=5*scale;
            ctx.beginPath(); ctx.moveTo(base.x,base.y); ctx.lineTo(tip.x,tip.y); ctx.stroke(); ctx.shadowBlur=0;
            var orbR=cp*24*scale;
            if (orbR>0 && isFinite(tip.x) && isFinite(tip.y)) {
                var g=ctx.createRadialGradient(tip.x,tip.y,0,tip.x,tip.y,orbR);
                g.addColorStop(0,'rgba(255,255,255,1)'); g.addColorStop(0.3,'rgba(0,243,255,0.8)'); g.addColorStop(1,'rgba(0,243,255,0)');
                ctx.fillStyle=g; ctx.beginPath(); ctx.arc(tip.x,tip.y,orbR,0,Math.PI*2); ctx.fill();
            }
        }
        // VFX: slash trail (55-65)
        if (idx>=55 && idx<=65) {
            ctx.shadowColor='#00f3ff'; ctx.shadowBlur=25; ctx.lineWidth=10*scale; ctx.lineCap='round'; ctx.lineJoin='round';
            ctx.beginPath();
            for (var i=55; i<=idx; i++) {
                var ci=getSwordCoords(i);
                var tx=dx+sx+ci.tip.x*scale, ty=dy+sy+ci.tip.y*scale;
                if (i===55) ctx.moveTo(tx,ty); else ctx.lineTo(tx,ty);
            }
            var sp=getSwordCoords(55).tip, x0=dx+sx+sp.x*scale, y0=dy+sy+sp.y*scale;
            if (isFinite(x0)&&isFinite(y0)&&isFinite(tip.x)&&isFinite(tip.y)) {
                var g2=ctx.createLinearGradient(x0,y0,tip.x,tip.y);
                g2.addColorStop(0,'rgba(0,243,255,0)'); g2.addColorStop(0.5,'rgba(0,243,255,0.6)'); g2.addColorStop(1,'rgba(255,255,255,0.95)');
                ctx.strokeStyle=g2; ctx.stroke();
            }
            ctx.shadowBlur=0;
        }
        if (idx>=55 && idx<=65 && Math.random()<0.8) {
            for (var k=0;k<4;k++) particles.push(new Particle(tip.x,tip.y,k%2===0?'#00f3ff':'#ff2e4d'));
        }
    }

    function updateParticles() {
        for (var i=particles.length-1;i>=0;i--) {
            particles[i].update();
            if (particles[i].life<=0) particles.splice(i,1);
            else particles[i].draw(ctx);
        }
    }

    function renderLoop() {
        if (!isLoaded) { requestAnimationFrame(renderLoop); return; }
        if (window.scrollY < 5) {
            idleFC += 0.35;
            var it = Math.floor(idleFC % 43);
            curFI += (it - curFI) * LERP;
        } else {
            curFI += (tgtFI - curFI) * LERP;
            if (curFI < 35) curFI = 35;
            if (curFI > 72) curFI = 72;
        }
        var ri = Math.floor(curFI);
        drawFrame(images[ri], ri);
        updateParticles();
        requestAnimationFrame(renderLoop);
    }

    function preloadImages(callback) {
        var loaded = 0;
        framePaths.forEach(function(src) {
            var img = new Image();
            img.onload = function() {
                loaded++;
                var pct = Math.round(loaded/framePaths.length*100);
                document.getElementById('loaderBar').style.width = pct + '%';
                document.getElementById('loaderText').innerText = 'PREPARING INTERACTION... ' + pct + '%';
                if (loaded === framePaths.length) { isLoaded = true; fadeLoader(callback); }
            };
            img.onerror = function() {
                loaded++;
                if (loaded === framePaths.length) { isLoaded = true; fadeLoader(callback); }
            };
            img.src = src;
            images.push(img);
        });
    }

    function fadeLoader(cb) {
        var l = document.getElementById('loader');
        l.style.opacity = '0';
        setTimeout(function() { l.style.display = 'none'; cb(); }, 500);
    }

    // SCROLL PROGRESS -> ANIMATION (remapped to 0-72 index range)
    function updateAnimationProgress(progress) {
        var ti = 35;
        if      (progress < 0.15) ti = 35 + (progress/0.15)*(43-35);
        else if (progress < 0.45) ti = 43 + ((progress-0.15)/0.30)*(55-43);
        else if (progress < 0.65) ti = 55 + ((progress-0.45)/0.20)*(65-55);
        else if (progress < 0.80) ti = 65 + ((progress-0.65)/0.15)*(72-65);
        else                      ti = 72;
        tgtFI = ti;
        var hc = document.getElementById('hero-content');
        if (progress < 0.15) {
            hc.style.opacity = 1 - progress/0.15;
            hc.style.transform = 'translateY(' + (-progress*200) + 'px) scale(' + (1-progress*0.08) + ')';
            hc.style.pointerEvents = 'auto';
        } else { hc.style.opacity = 0; hc.style.pointerEvents = 'none'; }
        var fr = document.getElementById('featuresReveal');
        if (progress < 0.45) {
            fr.style.clipPath = 'polygon(100% 0,100% 0,100% 100%,100% 100%)';
        } else if (progress <= 0.70) {
            var p = (progress-0.45)/0.25;
            var x1 = Math.max(0,100-p*130), x2 = Math.max(0,100-p*130+30);
            fr.style.clipPath = 'polygon('+x1+'% 0,100% 0,100% 100%,'+x2+'% 100%)';
        } else {
            if (window.scrollY < window.innerHeight*2) fr.style.clipPath = 'polygon(0 0,100% 0,100% 100%,0 100%)';
        }
    }

    // STICKY POSITION CONTROLLER
    window.addEventListener('scroll', function() {
        var sy = window.scrollY, th = window.innerHeight * 2;
        var fr = document.getElementById('featuresReveal');
        if (sy >= th) {
            fr.style.position = 'relative'; fr.style.marginTop = '200vh';
            fr.style.height = 'auto'; fr.style.overflow = 'visible';
            fr.style.clipPath = 'none'; fr.style.pointerEvents = 'auto';
        } else {
            fr.style.position = 'fixed'; fr.style.top = '0'; fr.style.marginTop = '0';
            fr.style.height = '100vh'; fr.style.overflow = 'hidden';
            fr.style.pointerEvents = sy > th*0.5 ? 'auto' : 'none';
        }
    });

    // BOOT
    preloadImages(function() {
        renderLoop();
        preloadCharFrames();
        gsap.registerPlugin(ScrollTrigger);
        var sp = { progress: 0 };
        gsap.to(sp, {
            progress: 1, ease: 'none',
            scrollTrigger: { trigger: '#scrollContainer', start: 'top top', end: 'bottom bottom', scrub: 1.0 },
            onUpdate: function() { updateAnimationProgress(sp.progress); }
        });
        document.querySelectorAll('.reveal').forEach(function(el, i) {
            el.dataset.delay = i * 150; revealObserver.observe(el);
        });
    });

    document.getElementById('playBtn').addEventListener('click', openCharModal);
</script>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(before + new_script)

print('SUCCESS - file written, total chars:', len(before + new_script))
