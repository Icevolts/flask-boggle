class BoggleGame{
    //start a new game at this id
    constructor(boardId,time = 60){
        this.words = new Set();
        this.board = $('#' + boardId);
        this.score = 0

        this.time = time
        this.showTimer();
        this.timer = setInterval(this.tick.bind(this), 1000);

        $('.add-word', this.board).on('submit', this.handleSubmit.bind(this));
    }

    // add word to the list of words
    addWord(word){
        $('.words', this.board).append($('<li>', {text : word}));
    }

    // show status message corresponding to the word entered
    showMessage(msg, cls){
        $('.msg', this.board).text(msg).removeClass().addClass(`msg ${cls}`)
    }

    showScore(){
        $('.score',this.board).text(this.score);
    }

    showTimer(){
        $('.timer',this.board).text(this.time);
    }

    async tick(){
        this.time -= 1;
        this.showTimer();

        if(this.time === 0){
            clearInterval(this.timer);
            await this.tallyScore();
        }
    }

    // click handler for entered word
    async handleSubmit(evt){
        evt.preventDefault();
        const $word = $('.word',this.board);
        let word = $word.val();
        
        // if not a word,do nothing
        if (!word) return;

        // if word already in list,tell player
        if(this.words.has(word)){
            this.showMessage(`You already found ${word}`,'err');
            return;
        }

        // check with server for word validity
        const res = await axios.get('/check-word', {params: {word : word}});
        if(res.data.result === 'not-word'){
            this.showMessage(`${word} is not a valid word`,'err');
        }else if(res.data.result === 'not-on-board'){
            this.showMessage(`${word} is not a valid word for this board`,'err');
        }else{
            this.addWord(word)
            this.words.add(word)
            this.showMessage(`${word} added successfully!`, 'ok');
            this.score += word.length;
            this.showScore();
        }
        $word.val("").focus();
    }

    async tallyScore(){
        $('.add-word', this.board).hide();
        const res = await axios.post('/scoring', {score : this.score});
        if(res.data.newRecord){
            this.showMessage(`New Record: ${this.score}`, 'ok')
        }else{
            this.showMessage(`Final Score: ${this.score}`, 'ok')
        }
    }
}
