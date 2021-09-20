
const root = document.documentElement;

const fretboard = document.querySelector('.fretboard');
const numberOfFretsSelector = document.querySelector('#number-of-frets');
const scaleSelector = document.querySelector('#scale');
const scaleKeySelector = document.querySelector('#scale-key')
const tuningSelector = document.querySelector("#tuningSelector");

let selectedScale = undefined;
let selectedScaleKey = undefined;
let numberOfFrets = 15;
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

                for (noteIdx=0; noteIdx<response.notes.length;noteIdx++){

                    let noteFret = tools.createElement('div');
                    noteFret.classList.add('note-fret');
                    string.appendChild(noteFret);

                    noteFret.setAttribute('data-note', response.notes[noteIdx].name);
                    noteFret.setAttribute('data-frequency', response.notes[noteIdx].frequency);

                    // add single fretmarks
                    if (stringIdx == 0 && singleFretMarkPositions.includes(noteIdx)){
                        noteFret.classList.add('single-fretmark');
                    }

                    // add double fretmarks
                    if (stringIdx == 0 && doubleFretMarkPositions.includes(noteIdx)){
                        let doubleFretMark = tools.createElement('div');
                        doubleFretMark.classList.add('double-fretmark');
                        noteFret.appendChild(doubleFretMark);
                    }
                }
            })
        }

        // add tunings
        $.get(`api/tunings`).done((response) => {

            for (tuning_idx=0;tuning_idx<response.length;tuning_idx++){
                // Create and append the options
                let option = document.createElement("option");
                option.value = response[tuning_idx]["notes"];
                option.text = `${response[tuning_idx]["name"]} - ${response[tuning_idx]["notes"]}`;
                tuningSelector.appendChild(option);
            }
            let option = document.createElement("option");
            option.value = "Custom";
            option.text = "Custom";
            tuningSelector.appendChild(option);
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

                            // setup event listener for dropdowns
                            clonedSelectList.addEventListener('change', (event) => {
                                let stringIdx = Array.from(event.target.parentNode.children).indexOf(event.target);
                                let note = `${event.target.value}`.replace(/#/g, "%23");
                                $.get(`api/string/${note}`).done((response)=> {
                                 for (noteIdx = 0; noteIdx < response.notes.length; noteIdx++) {
                                     strings[stringIdx].children[noteIdx].setAttribute("data-note", response.notes[noteIdx].name)
                                    }
                                })
                            });
                        }
                    });
                }
                customTuningContainer.style.setProperty('visibility', 'visible');
            }else{
                customTuningContainer.style.setProperty('visibility', 'hidden');

                const openNotes = event.target.value.replace(/#/g, "%23").split(",");

                // iterate through notes in tuning and update strings
                for (let stringIdx=0;stringIdx<numberOfStrings;stringIdx++){
                    $.get(`api/string/${openNotes[stringIdx]}`).done((response)=> {
                         for (noteIdx = 0; noteIdx < response.notes.length; noteIdx++) {
                             strings[stringIdx].children[noteIdx].setAttribute("data-note", response.notes[noteIdx].name)
                            }
                        })
                }
            }
        })
    },

    notesSelect(openNote){
        const notes = [openNote.dataset.note, 'A3', 'B3', 'C3', 'D2'];
        let selectList = document.createElement('select');

        // Create and append the options
        for (var i = 0; i < notes.length; i++) {
            var option = document.createElement("option");
            option.value = notes[i];
            option.text = notes[i];
            selectList.appendChild(option);
        }

        return selectList;
    },

    setupOpenNoteSelectors(openNote, string, stringIdx){
        const openNotesElement = document.querySelector('#openNotes');
        let selectList = this.notesSelect(openNote);
        selectList.style.setProperty('order', stringIdx)
        openNotesElement.appendChild(selectList);
        selectList.addEventListener("change", (event) => {
            openNote.setAttribute('data-note', event.target.value)
             $.get(`api/string/${event.target.value}`).done((response)=> {
                 for (noteIdx = 0; noteIdx < response.notes.length; noteIdx++) {
                     string.children[noteIdx].setAttribute("data-note", response.notes[noteIdx].name)
                 }
             })
        })
    },

    getScale(){
        // turn notes off
        for (let stringIdx =0; stringIdx < numberOfStrings; stringIdx++){
                for (let fret_idx=0;fret_idx<numberOfFrets;fret_idx++){
                    fretboard.children[stringIdx].children[fret_idx].style.setProperty('--noteDotOpacity', 0)
                }
            }

        // use notes from the dom to retrive a scale
        let openNotes = Array.from(document.getElementById("openNotes").children).sort((a, b)=> a.style.order - b.style.order).map(g => g.value).toString()
        console.log(`openNotes: ${openNotes}`)
        $.get(`api/scale/${selectedScale}/?key=${selectedScaleKey}&tuning=${openNotes}`).done((response)=>{

            // turn notes on for new scale
            for (let stringIdx =0; stringIdx < numberOfStrings; stringIdx++){
                for (let fret_idx=0;fret_idx<response[0].notes.length;fret_idx++){
                    if (response[stringIdx].notes[fret_idx].is_apart_of_scale === true){
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
            function change() {

                if (setIntervalIndex === fretboardLowString.length){
                    clearInterval(timer);
                    fretboardLowString[prevIndex].style.setProperty('--noteColour', "teal")
                    return;
                }

                if (response[0].notes[setIntervalIndex].is_apart_of_scale === true){
                    time_offset = time_offset + 0.5

                    if (prevIndex !== undefined){
                        fretboardLowString[prevIndex].style.setProperty('--noteColour', "teal")
                    }
                    fretboardLowString[setIntervalIndex].style.setProperty('--noteColour', "yellow")
                    instruments_.triggerAttackRelease(response[numberOfStrings-1].notes[setIntervalIndex].name, 0.2, now+time_offset)
                    prevIndex = setIntervalIndex
                }
                setIntervalIndex = setIntervalIndex + 1;

            }
            const timer = setInterval(change, 200);
        });
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