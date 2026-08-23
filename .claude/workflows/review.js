export const meta = {
  name: 'review',
  description: 'Fan out bug finders per module, adversarially refute each finding',
  phases: [
    { title: 'Find', detail: 'one finder agent per module' },
    { title: 'Refute', detail: 'one adversarial verifier per finding', model: 'haiku' },
  ],
}

const BUGS = {
  type: 'object',
  properties: {
    bugs: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          file: { type: 'string' },
          line: { type: 'number' },
          desc: { type: 'string' },
        },
        required: ['file', 'desc'],
      },
    },
  },
  required: ['bugs'],
}

const VERDICT = {
  type: 'object',
  properties: {
    real: { type: 'boolean' },
    why: { type: 'string' },
  },
  required: ['real', 'why'],
}

const DIRS = ['api', 'web', 'jobs']

phase('Find')
const found = await parallel(DIRS.map(d => () =>
  agent(
    `Read every Python file under ${d}/ in this repo and report genuine logic bugs ` +
    '(wrong results, silently swallowed failures). Ignore style issues. ' +
    'Report an empty list if the code is correct.',
    { label: `find:${d}`, phase: 'Find', schema: BUGS },
  )))

const bugs = found.filter(Boolean).flatMap(r => r.bugs)
log(`${bugs.length} candidate finding(s)`)

phase('Refute')
const judged = await parallel(bugs.map(b => () =>
  agent(
    `Adversarially verify this bug report about ${b.file}` +
    (b.line ? `:${b.line}` : '') +
    `: "${b.desc}". Read the file, including docstrings and comments. ` +
    'If the behavior is intentional or actually correct, refute the report.',
    { label: `refute:${b.file}`, phase: 'Refute', schema: VERDICT, model: 'haiku' },
  ).then(v => v && { ...b, ...v })))

const confirmed = judged.filter(Boolean).filter(j => j.real)
const refuted = judged.filter(Boolean).filter(j => !j.real)
log(`${confirmed.length} confirmed · ${refuted.length} refuted`)
return { confirmed, refuted }
