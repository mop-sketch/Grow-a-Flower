from random import random, shuffle
from pyscript import when
from pyscript.web import page
from js import document
import asyncio


water = 50
fertilizer = 0
sunlight = 50
growth_stage = 0
dead = False
heat_wave_ticks = 0
rainstorm_ticks = 0
health = 100
pest_active = False
warmth_button_shown = False
warmth = 50
mystery_menu = False
menu_open = False

upgrades = {"decay": 0, "fertilizer": 0, "safe_zone": 0, "weather": 0}
current_upgrade_choices = []

UPGRADE_INFO = {
    "decay":      ("Slow Decay",       "Water, sunlight & warmth decay −0.5/tick per level"),
    "fertilizer": ("Boost Fertilizer", "Fertilizer generation +1/tick per level"),
    "safe_zone":  ("Widen Safe Zone",  "Fertilizer safe zone expands 5% per level"),
    "weather":    ("Weather Shield",   "Heat wave & rainstorm intensity −1/tick per level"),
}
MAX_UPGRADE_LEVEL = 3

STAGES = [
    "flower/Seed.png",
    "flower/Sprout.png",
    "flower/Seedling.png",
    "flower/YoungPlant.png",
    "flower/OlderPlant.png",
    "flower/Budding.png",
    "flower/Flowering.png",
]
FINAL_STAGE = len(STAGES) - 1

def advance_stage():
    global growth_stage, fertilizer
    if growth_stage < FINAL_STAGE:
        growth_stage += 1
        fertilizer = 0
        grow_audio = document.getElementById("grow-audio")
        grow_audio.currentTime = 0
        grow_audio.play()


def show_upgrade_menu():
    global mystery_menu, current_upgrade_choices
    available = [k for k, v in upgrades.items() if v < MAX_UPGRADE_LEVEL]
    shuffle(available)
    current_upgrade_choices = available[:3]
    document.body.classList.remove("winter", "heat-wave", "rainstorm")

    card_ids = ["upgrade-option", "upgrade-option1", "upgrade-option2"]
    for i, card_id in enumerate(card_ids):
        card = document.getElementById(card_id)
        if i < len(current_upgrade_choices):
            key = current_upgrade_choices[i]
            name, desc = UPGRADE_INFO[key]
            level = upgrades[key]
            stars = "★" * level + "☆" * (MAX_UPGRADE_LEVEL - level)
            card.innerHTML = (
                f'<h3 style="margin:0 0 4px 0;color:#000000;font-size:14px;">{name}</h3>'
                f'<div style="color:#654321;font-size:18px;margin-bottom:6px;">{stars}</div>'
                f'<p style="color:#000000;font-size:11px;margin:0 0 4px 0;text-align:center;">{desc}</p>'
                f'<p style="color:#ffffff;font-size:11px;margin:0 0 10px 0;">Level {level} \u2192 {level + 1}</p>'
                f'<button class="upgrade-button" id="upgrade-btn-{i}">Choose</button>'
            )
            card.style.display = "flex"
            card.style.flexDirection = "column"
            card.style.alignItems = "center"
            card.style.justifyContent = "center"
            card.style.padding = "10px"
            btn = document.getElementById(f"upgrade-btn-{i}")
            btn.onclick = lambda e, idx=i: select_upgrade(idx)
        else:
            card.innerHTML = ""
            card.style.display = "none"

    document.getElementById("upgrade-container").style.display = "block"
    mystery_menu = True


def select_upgrade(index):
    global mystery_menu
    if index < len(current_upgrade_choices):
        key = current_upgrade_choices[index]
        upgrades[key] = min(upgrades[key] + 1, MAX_UPGRADE_LEVEL)
    mystery_menu = False
    document.getElementById("upgrade-container").style.display = "none"
    asyncio.ensure_future(decay_loop())


def get_bar_color(value, default_color):
    if value <= 30 or value >= 75:
        return "#ff7867"
    elif value <= 40 or value >= 65:
        return "#fff569"
    else:
        return default_color

def update_status():
    
    global water, fertilizer, sunlight, growth_stage, dead, heat_wave_ticks, rainstorm_ticks, health, pest_active, mystery_menu
    if FINAL_STAGE == growth_stage or mystery_menu or menu_open:
        return
    
    flower_image = page["#flower-image"]
    water_bar = document.getElementById("water-bar")
    sun_bar = document.getElementById("sun-bar")
    health_row = document.getElementById("health-row")
    warmth_bar = document.getElementById("warmth-bar")
    
    water_bar.style.backgroundColor = get_bar_color(water, "#6cf38e")
    sun_bar.style.backgroundColor = get_bar_color(sunlight, "#6cf38e")
    warmth_bar.style.backgroundColor = get_bar_color(warmth, "#6cf38e")
    warmth_bar.style.width = f"{warmth}%"
    water_bar.style.width = f"{water}%"
    sun_bar.style.width = f"{sunlight}%"
    health_bar = document.getElementById("health-bar")
    health_bar.style.width = f"{health}%"
    
    if pest_active and sunlight >= 70:
        health_row.style.display = "none"
        pest_active = False
        document.body.classList.remove("health-active")
    if heat_wave_ticks > 0:
        page["#status"].innerHTML = f"🌡️ Heat wave! ({heat_wave_ticks}s remaining)"
    elif health == 0:
        dead = True
        flower_image.src = "flower/DeadPlant.png"
        page["#status"].innerHTML = "Plant has died due to poor health❤️. Restart to try again."
    elif pest_active and not dead:
        page["#status"].innerHTML = "Pests are active🐛! Add sunlight to burn them off."
    elif rainstorm_ticks > 0:
        page["#status"].innerHTML = f"🌧️ Rainstorm! ({rainstorm_ticks}s remaining)"
    elif fertilizer >= (30 if growth_stage == 0 else 70) and (water >= 40 and water <= 65) and (sunlight >= 40 and sunlight <= 65):
        page["#status"].innerHTML = "Fertilizer at safe levels✅"
    elif fertilizer >= (30 if growth_stage == 0 else 70) and (water <= 40 or water >= 65 or sunlight <= 40 or sunlight >= 65):
        page["#status"].innerHTML = "Fertillizer ready, but other conditions are not optimal❌"
    else:
        page["#status"].innerHTML = f"Fertilizer is at unsafe levels❌"
    if heat_wave_ticks > 0:
        document.body.classList.remove("winter")
        document.body.classList.add("heat-wave")
    else:
        document.body.classList.remove("heat-wave")
    if rainstorm_ticks > 0:
        document.body.classList.remove("winter")
        document.body.classList.add("rainstorm")
    else:
        document.body.classList.remove("rainstorm")
    if growth_stage >= 3:
        if heat_wave_ticks == 0 and rainstorm_ticks == 0:
            document.body.classList.add("winter")
    else:
        document.body.classList.remove("winter")
    
    if water <= 15 or sunlight <= 15 or water >= 90 or sunlight >= 90 or (warmth <= 15 or warmth >= 90):
        dead = True
        flower_image.src = "flower/DeadPlant.png"
        document.body.classList.remove("heat-wave", "rainstorm", "winter")
        page["#status"].innerHTML = "Plant has died. Restart to try again."
        if growth_stage == 0:
            flower_image.src = STAGES[0]
            page["#status"].innerHTML = "Plant has failed to germinate"
    else:
        flower_image.src = STAGES[growth_stage]
@when("click", "#water-btn")
def on_water(event):
    if dead:
        return
    global water, fertilizer
    water = min(water + 5, 100)
    fertilizer = min(fertilizer + 1, 100)
    update_status()

@when("click", "#sun-btn")
def on_sunlight(event):
    
    if dead:
        return
    global sunlight, fertilizer
    sunlight = min(sunlight + 5, 100)
    fertilizer = min(fertilizer + 1, 100)
    update_status()

@when("click", "#fertilizer-btn")
def on_fertilizer(event):
    if dead:
        return
    global fertilizer, water, sunlight, mystery_menu
    lore_btn = document.getElementById("lore-btn")
    control = document.getElementById("controls-container")
    threshold = 30 if growth_stage == 0 else 70
    safe_min = max(35 - upgrades["safe_zone"] * 5, 15)
    safe_max = min(70 + upgrades["safe_zone"] * 5, 90)
    if fertilizer >= threshold and (water >= safe_min and water <= safe_max) and (sunlight >= safe_min and sunlight <= safe_max):
        advance_stage()
        if growth_stage == FINAL_STAGE:
            lore_btn.innerText = "Touch the flower"
            win_audio = document.getElementById("win-audio")
            win_audio.currentTime = 0
            win_audio.play()
            document.body.classList.remove("winter", "heat-wave", "rainstorm")
            document.body.classList.add("spring")
            control.style.display = "none"
            page["#flower-image"].src = STAGES[FINAL_STAGE]
            page["#status"].innerHTML = "🌸 Your flower has fully bloomed! You win!"
            from js import launchConfetti
            launchConfetti()

        else:
            update_status()
            show_upgrade_menu()
    else:
        water = max(water - 50, 0)
        sunlight = max(sunlight - 50, 0)
        update_status()
@when("click", "#warmth-btn") 
def on_warmth(event):
    if dead:
        return
    global warmth
    warmth = min(warmth + 5, 100)
    update_status()
@when("click", "#main-menu-btn")
def on_main_menu(event):
    global menu_open
    menu_container = document.getElementById("menu-container")
    if menu_open:
        menu_container.style.display = "none"
        menu_open = False
    else:
        document.body.classList.remove("winter", "heat-wave", "rainstorm")
        menu_open = True
        menu_container.style.display = "block"
@when("click", "#restart-btn")
def on_restart(event):
    document.body.classList.remove("winter", "heat-wave", "rainstorm")
    document.location.reload()
@when("click", "#lore-btn")
def on_lore(event):
    menu_container = document.getElementById("menu-container")
    flower_image = document.getElementById("flower")
    global growth_stage
    if growth_stage == FINAL_STAGE:
        grow_audio = document.getElementById("grow-audio")
        grow_audio.currentTime = 0
        grow_audio.play()
        dark_audio = document.getElementById("dark-audio")
        dark_audio.currentTime = 0
        dark_audio.playbackRate = 2
        dark_audio.play()
        page["#status"].innerHTML = "Error Code: Unknown"
        document.body.classList.remove("spring")
        document.body.classList.add("lore-mode")
        from js import glitchTitle
        glitchTitle()
        menu_container.style.display = "none"
        springs = document.getElementById("spring1")
        springs2 = document.getElementById("spring2")
        flower_image.innerHTML = "<p class='spinning-gear'>⚙</p>"
        springs.style.display = "block"
        springs2.style.display = "block"

async def decay_loop():
    health_bar = document.getElementById("health-row")
    sun_btn = document.getElementById("sun-btn")
    water_btn = document.getElementById("water-btn")
    warmth_btn = document.getElementById("warmth-btn")
    warmth_row = document.getElementById("warmth-row")

    global water, fertilizer, sunlight, health, heat_wave_ticks, rainstorm_ticks, pest_active, warmth_button_shown, warmth
    while True:
        await asyncio.sleep(1)
        
        if growth_stage == 3 and warmth_button_shown == False:
            sun_btn.style.left = "15%"
            water_btn.style.left = "85%"

            warmth_btn.style.display = "block"
            warmth_row.style.display = "flex"
            warmth_button_shown = True
            document.body.classList.add("warmth-active")
        if dead or growth_stage == FINAL_STAGE or mystery_menu:
            break
        if menu_open:
            continue
        if not pest_active and random() < 0.01 and heat_wave_ticks == 0 and rainstorm_ticks == 0 and growth_stage > 0:
            health_bar.style.display = "flex"
            pest_active = True
            document.body.classList.add("health-active")
        if rainstorm_ticks == 0 and random() < 0.01 and heat_wave_ticks == 0 and not pest_active:
            rainstorm_ticks = 4
        if heat_wave_ticks == 0 and random() < 0.01 and rainstorm_ticks == 0 and not pest_active:
            heat_wave_ticks = 4
        if water >= 70:
            sunlight = max(sunlight - 3, 0)
        if sunlight >= 70:
            water = max(water - 3, 0)
        if pest_active:
            health = max(health - 3, 0)
        weather_intensity = max(4 - upgrades["weather"], 1)
        if heat_wave_ticks > 0:
            sunlight = min(sunlight + weather_intensity, 100)
            water = max(water - weather_intensity, 0)
            heat_wave_ticks -= 1
            if growth_stage >= 3:
                warmth = min(warmth + weather_intensity, 100)
        decay = max(2 - upgrades["decay"] * 0.5, 0.25)
        if growth_stage >= 3:
            warmth = max(warmth - decay, 0)
        if rainstorm_ticks > 0:
            water = min(water + weather_intensity, 100)
            sunlight = min(sunlight - weather_intensity, 100)
            rainstorm_ticks -= 1
        water = max(water - decay, 0)
        if growth_stage < FINAL_STAGE:
            fertilizer = min(fertilizer + 3 + upgrades["fertilizer"], 100)
        sunlight = max(sunlight - decay, 0)
        update_status()

asyncio.ensure_future(decay_loop())