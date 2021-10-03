
const root = document.documentElement;

const fretboard = document.querySelector('.fretboard');
const numberOfFretsSelector = document.querySelector('#number-of-frets');
const scaleSelector = document.querySelector('#scaleSelector');
const scaleKeySelector = document.querySelector('#scaleKeySelector')
const tuningSelector = document.querySelector("#tuningSelector");

let selectedScale = undefined;
let selectedScaleKey = undefined;
let numberOfFrets = 12 + 1;
let instruments_ = Instruments.handle();
const numberOfStrings = 6;
const singleFretMarkPositions = [3, 5, 7, 9, 15, 17, 19, 21];
const doubleFretMarkPositions = [12, 24];

const defaultStringOpenNotes = ["E4", "B3", "G3", "D3", "A2", "E2"]

const strings = [];

const app = {
    init(){
        this.setupFretboard();
        this.setupEventListeners();
    },
    setupFretboard(){
        fretboard.innerHTML = "";
        root.style.setProperty('--number-of-strings', numberOfStrings);

        // add strings
        for (let stringIdx =0; stringIdx < numberOfStrings; stringIdx++){
            let string = tools.createElement('div');
            string.classList.add('string');
            fretboard.appendChild(string);

            // get string from api
            $.get(`api/string/${defaultStringOpenNotes[stringIdx]}`).done((response)=>{

                for (noteIdx=0; noteIdx<response.frets.length;noteIdx++){

                    let noteFret = tools.createElement('div');
                    noteFret.classList.add('note-fret');
                    string.appendChild(noteFret);
                    noteFret.setAttribute('data-note', response.frets[noteIdx].note);

                    // add single fretmarks
                    if (stringIdx === 0 && singleFretMarkPositions.includes(noteIdx)){
                        noteFret.classList.add('single-fretmark');
                    }

                    // add double fretmarks
                    if (stringIdx === 0 && doubleFretMarkPositions.includes(noteIdx)){
                        let doubleFretMark = tools.createElement('div');
                        doubleFretMark.classList.add('double-fretmark');
                        noteFret.appendChild(doubleFretMark);
                    }
                }
            })
        }

        // add tunings to selector
        $.get(`api/tunings`).done((response) => {

            let tuningCategories = {};
            // first organise into categories
            for (tuningIdx=0;tuningIdx<response.length;tuningIdx++) {
                if (!(response[tuningIdx]["category"] in tuningCategories)) {
                    tuningCategories[response[tuningIdx]["category"]] = []
                }
                tuningCategories[response[tuningIdx]["category"]].push(response[tuningIdx])
            }
            // then create the categories and options
            Object.entries(tuningCategories).forEach(([key, value]) => {
                let optGroup = document.createElement("optgroup");
                optGroup.label = key
                value.forEach(value => {
                    let option = document.createElement("option");
                    option.value = value["notes"];
                    option.text = `${value["name"]} - ${value["notes"]}`;
                    optGroup.appendChild(option)
                })
                tuningSelector.appendChild(optGroup);
            })
            // finally add a custom option
            let customOptGroup = document.createElement("optgroup");
            customOptGroup.label = "Custom"
            let customOption = document.createElement("option");
            customOption.value = "Custom"
            customOption.text = "Custom"
            customOptGroup.appendChild(customOption)
            tuningSelector.appendChild(customOptGroup)
        })

        // add scales to selector
        $.get(`api/scales`).done((response) => {
            for (scaleIdx=0; scaleIdx<response.length;scaleIdx++){
                let option = document.createElement("option");
                option.value = response[scaleIdx]["name"];
                option.text = response[scaleIdx]["name"];
                scaleSelector.appendChild(option);
            }
        })
        // add scale keys to selector
        $.get('api/notes/?keys_only=True').done((response) => {
            for (keyIdx=0; keyIdx<response.length;keyIdx++){
                let option = document.createElement("option");
                option.value = response[keyIdx]["name"];
                option.text = response[keyIdx]["name"];
                scaleKeySelector.appendChild(option);
            }
        })
    },
    setupEventListeners(){
        fretboard.addEventListener('mouseover', (event) => {
            if (event.target.classList.contains('note-fret')){
                event.target.style.setProperty('--noteDotOpacity', 0.5);

                let note = $(event.target).attr("data-note");
                instruments_.triggerAttack(`${note}`);
            }
        })
        fretboard.addEventListener('mouseout', (event) => {
            event.target.style.setProperty('--noteDotOpacity', 0);
            if (event.target.classList.contains('note-fret')){
                let note = $(event.target).attr("data-note");
                instruments_.triggerRelease(`${note}`);

            }
        })
        numberOfFretsSelector.addEventListener('change', (event) => {
            numberOfFrets = numberOfFretsSelector.value;
            this.setupFretboard();
        })

        // To get the scale, both the scale and key must be entered
        scaleSelector.addEventListener('change', (event)=> {
            selectedScale = scaleSelector.value;
            if (selectedScaleKey !== undefined){
                this.getScale();
            }
        })
        scaleKeySelector.addEventListener('change', (event) => {
            selectedScaleKey = scaleKeySelector.value;
            if (selectedScale !== undefined){
                this.getScale();
            }
        })
        // update the strings with the tunings
        // if custom is chosen, display selectors for each string
        tuningSelector.addEventListener('change', (event) => {
            let strings = document.querySelectorAll(".string");

            if (event.target.value === "Custom"){
                // display selectors for notes
                const customTuningContainer = document.querySelector("#customTuningContainer");

                if (customTuningContainer.childElementCount === 0){
                    $.get(`api/notes`).done((response) => {

                        // put all notes into 1 select
                        let selectList = document.createElement('select');
                        for (let noteIdx = 0; noteIdx < response.length; noteIdx++){
                            let option = document.createElement("option");
                            option.value = response[noteIdx]['name'];
                            option.text = response[noteIdx]['name'];
                            selectList.appendChild(option);
                        }
                        // now copy the selectList for n strings into the customTuningContainer div
                        for (stringIdx=0;stringIdx<numberOfStrings ;stringIdx++) {
                            let clonedSelectList = selectList.cloneNode(true)
                            customTuningContainer.appendChild(clonedSelectList);

                            // setup event listener for dropdowns so we can update the string everytime we select
                            // a note
                            clonedSelectList.addEventListener('change', (event) => {

                                // find the selected string index
                                let numOfStrings = Array.from(event.target.parentNode.children).length
                                let stringIdx = (numOfStrings - Array.from(event.target.parentNode.children).indexOf(event.target)) - 1;

                                let note = `${event.target.value}`.replace(/#/g, "%23");
                                $.get(`api/string/${note}`).done((response)=> {
                                 for (noteIdx = 0; noteIdx < response.frets.length; noteIdx++) {
                                     strings[stringIdx].children[noteIdx].setAttribute("data-note", response.frets[noteIdx].note)
                                    }
                                })
                            });
                        }
                    });
                }
                customTuningContainer.style.setProperty('visibility', 'visible');
            }else{
                customTuningContainer.style.setProperty('visibility', 'hidden');

                // Note we reverse the notes as
                const openNotes = event.target.value.replace(/#/g, "%23").split(",").reverse();

                // iterate through notes in tuning and update strings
                for (let stringIdx=0;stringIdx<numberOfStrings;stringIdx++){
                    $.get(`api/string/${openNotes[stringIdx]}`).done((response)=> {
                         for (noteIdx = 0; noteIdx < response.frets.length; noteIdx++) {
                             strings[stringIdx].children[noteIdx].setAttribute("data-note", response.frets[noteIdx].note)
                            }
                        })
                }
            }
            this.clearBoard();
        })
    },

    getScale(){
        // turn notes off
        this.clearBoard()

        // use notes from the dom to retrieve a scale
        let openNotes = Array.from(document.querySelectorAll(".string")).map(string => string.firstElementChild.dataset.note).toString().replace(/#/g, "%23")
        console.log(`api/fretboard/tuning=${openNotes}&scale=${selectedScale}&key=${selectedScaleKey}`);
        $.get(`api/fretboard/${openNotes}?scale=${selectedScale}&key=${selectedScaleKey.replace(/#/g, "%23")}`).done((response)=>{
            // turn notes on for new scale
            for (let stringIdx =0; stringIdx < response.strings.length; stringIdx++){
                for (let fret_idx=0;fret_idx<response.strings[stringIdx].frets.length;fret_idx++){
                    if (response.strings[stringIdx].frets[fret_idx].meta.is_in_scale === true){
                        fretboard.children[stringIdx].children[fret_idx].style.setProperty('--noteColour', 'teal')
                        fretboard.children[stringIdx].children[fret_idx].style.setProperty('--noteDotOpacity', 1)
                    }
                    if (response.strings[stringIdx].frets[fret_idx].meta.is_root_note === true){
                        fretboard.children[stringIdx].children[fret_idx].style.setProperty('--noteColour', '#5a185a')
                        fretboard.children[stringIdx].children[fret_idx].style.setProperty('--noteDotOpacity', 1)
                    }
                }
            }

            // play sounds and highlight
            const now = Tone.now();
            let setIntervalIndex = 0;
            let time_offset = 0;
            let fretboardLowString = fretboard.children[numberOfStrings-1].children;
            let prevIndex = undefined;
            let prevColour = undefined;


            function change() {

                // when at the end clear the timer
                if (setIntervalIndex === fretboardLowString.length){
                    clearInterval(timer);
                    fretboardLowString[prevIndex].style.setProperty('--noteColour', prevColour)
                    return;
                }

                if (response.strings[0].frets[setIntervalIndex].meta.is_in_scale === true){
                    time_offset = time_offset + 0.5
                    if (prevIndex !== undefined){
                        fretboardLowString[prevIndex].style.setProperty('--noteColour', prevColour)
                    }
                    prevColour = getComputedStyle(fretboardLowString[setIntervalIndex]).getPropertyValue('--noteColour');
                    prevIndex = setIntervalIndex

                    fretboardLowString[setIntervalIndex].style.setProperty('--noteColour', "yellow")
                    instruments_.triggerAttackRelease(response.strings[numberOfStrings-1].frets[setIntervalIndex].note, 0.2, now+time_offset)


                }
                setIntervalIndex = setIntervalIndex + 1;

            }
            const timer = setInterval(change, 200);
        });
    },

    clearBoard(){
        // Remove  all notes from the fret board
        for (let stringIdx =0; stringIdx < numberOfStrings; stringIdx++){
                for (let fret_idx=0;fret_idx<numberOfFrets;fret_idx++){
                    fretboard.children[stringIdx].children[fret_idx].style.setProperty('--noteDotOpacity', 0)
                    fretboard.children[stringIdx].children[fret_idx].style.setProperty('--noteColour', 'teal')

                }
            }
    }




}

const tools = {
    createElement(element, content){
        element = document.createElement(element);
        if (content){
            element.innerHTML = content;
        }
        return element;
    }
}


app.init();