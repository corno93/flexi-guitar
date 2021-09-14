
const root = document.documentElement;

const fretboard = document.querySelector('.fretboard');
const numberOfFretsSelector = document.querySelector('#number-of-frets');
const scaleSelector = document.querySelector('#scale');
const scaleKeySelector = document.querySelector('#scale-key')

let selectedScale = undefined;
let selectedScaleKey = undefined;
let numberOfFrets = 15;
let instruments_ = Instruments.handle();
const numberOfStrings = 6;
const singleFretMarkPositions = [3, 5, 7, 9, 15, 17, 19, 21];
const doubleFretMarkPositions = [12, 24];

const stringOpenNotes = ["E4", "B3", "G3", "D3", "A2", "E2"]

const app = {
    init(){
        this.setupFretboard();
        this.setupEventListeners();
    },
    setupFretboard(){
        fretboard.innerHTML = "";
        root.style.setProperty('--number-of-strings', numberOfStrings);

        // add strings
        for (let string_idx =0; string_idx < numberOfStrings; string_idx++){
            let string = tools.createElement('div');
            string.classList.add('string');
            fretboard.appendChild(string);

            // get string from api
            $.get(`api/string/${stringOpenNotes[string_idx]}`).done((response)=>{

                for (note_idx=0; note_idx<response.notes.length;note_idx++){

                    let noteFret = tools.createElement('div');
                    noteFret.classList.add('note-fret');
                    string.appendChild(noteFret);

                    noteFret.setAttribute('data-note', response.notes[note_idx].name);
                    noteFret.setAttribute('data-frequency', response.notes[note_idx].frequency);

                    // add single fretmarks
                    if (string_idx == 0 && singleFretMarkPositions.includes(note_idx)){
                        noteFret.classList.add('single-fretmark');
                    }

                    // add double fretmarks
                    if (string_idx == 0 && doubleFretMarkPositions.includes(note_idx)){
                        let doubleFretMark = tools.createElement('div');
                        doubleFretMark.classList.add('double-fretmark');
                        noteFret.appendChild(doubleFretMark);
                    }

                    // when first note, add event listener for changing note
                    if (note_idx === 0){
                        this.setupOpenNote(noteFret);
                    }
                }
            })
        }
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
    },

    notesSelect(openNote){
        const notes = [openNote.dataset.note, 'A', 'B', 'C', 'D'];
        let selectList = document.createElement('select');

        // Create and append the options
        for (var i = 0; i < notes.length; i++) {
            var option = document.createElement("option");
            option.value = notes[i];
            option.text = notes[i];
            selectList.appendChild(option);
        }

        selectList.addEventListener("change", (event) => {
            openNote.setAttribute('data-note', event.target.value)
        })

        return selectList;
    },

    setupOpenNote(openNote){
        const openNotesElement = document.querySelector('#openNotes');
        openNotesElement.appendChild(this.notesSelect(openNote));

    },

    getScale(){
        // turn notes off
        for (let string_idx =0; string_idx < numberOfStrings; string_idx++){
                for (let fret_idx=0;fret_idx<numberOfFrets;fret_idx++){
                    fretboard.children[string_idx].children[fret_idx].style.setProperty('--noteDotOpacity', 0)
                }
            }

        // get notes from doc
        $.get(`api/scale/${selectedScale}/?key=${selectedScaleKey}&tuning=E4,B3,G3,D3,A2,E2`).done((response)=>{

            // turn notes on for new scale
            for (let string_idx =0; string_idx < numberOfStrings; string_idx++){
                for (let fret_idx=0;fret_idx<response[0].notes.length;fret_idx++){
                    if (response[string_idx].notes[fret_idx].is_apart_of_scale === true){
                        fretboard.children[string_idx].children[fret_idx].style.setProperty('--noteDotOpacity', 1)
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