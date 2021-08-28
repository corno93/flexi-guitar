
const root = document.documentElement;

const fretboard = document.querySelector('.fretboard');
const numberOfFretsSelector = document.querySelector('#number-of-frets');
const toneJs = window.Tone;

let numberOfFrets = 17;
const numberOfStrings = 6;
const singleFretMarkPositions = [3, 5, 7, 9, 15, 17, 19, 21];
const doubleFretMarkPositions = [12, 24];

const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const guitarTunings = [4, 11, 7, 2, 9, 4]; // standard e tuning
const stringOpenNotes = ["E4", "B3", "G3", "D3", "A2", "E2"]

const app = {
    init(){
        const instruments = this.setupTone();
        this.setupFretboard();
        this.setupEventListeners(instruments);
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
                }
            })
        }
    },
    setupEventListeners(instruments){
        fretboard.addEventListener('mouseover', (event) => {
            if (event.target.classList.contains('note-fret')){
                event.target.style.setProperty('--noteDotOpacity', 0.5);

                let note = $(event.target).attr("data-note");

                let now = Tone.now()
                instruments.triggerAttack(`${note}`);
            }
        })
        fretboard.addEventListener('mouseout', (event) => {
            event.target.style.setProperty('--noteDotOpacity', 0);
            if (event.target.classList.contains('note-fret')){
                let note = $(event.target).attr("data-note");
                instruments.triggerRelease(`${note}`);

            }
        })
        numberOfFretsSelector.addEventListener('change', (event) => {
            numberOfFrets = numberOfFretsSelector.value;
            this.setupFretboard();
        })
    },

    setupTone(){
        return Instruments.handle()
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