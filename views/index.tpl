% rebase('base.tpl', title='Jisho to Anki')
<h1>Jisho to Anki</h1>
<input type="text" id="query" class="u-full-width" placeholder="English, Japanese, Romaji, words or text">
<div class="center">
  <div id="spinner" class="spinner hidden"></div>
</div>
<div id="response-display" hidden>
  <a id="add" class="button button-primary u-full-width">Add to Anki</a>
  <hr>
  <h2 id="word"></h2>
  <h4 id="reading"></h4>
  <section id="meaning"></section>
</div>

<script>
const query = document.getElementById('query')
const spinner = document.getElementById('spinner')
const responseDisplay = document.getElementById('response-display')
const add = document.getElementById('add')
const word = document.getElementById('word')
const reading = document.getElementById('reading')
const meaning = document.getElementById('meaning')

const search = async (term) => {
  const response = await fetch('/search/' + encodeURIComponent(term))
  const result = await response.json()
  if (!result.note) {
    return false
  }

  add.href = result.url
  const note = result.note
  word.textContent = note.{{config.word_field}}
  reading.textContent = note.{{config.reading_field}}
  meaning.innerHTML = note.{{config.meaning_field}}
  return true
}

const showElement = (element, show) => {
  if (show) {
    element.classList.remove('hidden')
  } else {
    element.classList.add('hidden')
  }
}

query.addEventListener('change', async (event) => {
  showElement(spinner, true)
  responseDisplay.hidden = true
  const hasResult = await search(query.value)
  showElement(spinner, false)
  responseDisplay.hidden = !hasResult
})
</script>