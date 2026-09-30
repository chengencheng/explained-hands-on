// StudyCrew matching and input checks. Pure functions only, so they are easy to test (see test/).

export const SUBJECTS = ["Math", "Physics", "Chemistry", "Biology", "English", "Chinese", "History", "Geography"];
export const SLOTS = ["Mon 4 pm", "Tue 4 pm", "Wed 4 pm", "Thu 4 pm", "Fri 4 pm", "Sat 10 am", "Sun 10 am"];
export const MAX_GROUP = 4;

// Check and clean what the browser sent. Never trust it: the browser is under the user's control.
// Returns { ok: true, value } or { ok: false, error }.
export function validateSignup(input) {
  if (!input || typeof input !== "object") return { ok: false, error: "Missing form data." };
  const clean = s => (typeof s === "string" ? s.trim().replace(/\s+/g, " ") : "");
  const firstName = clean(input.firstName);
  const className = clean(input.className);
  const subject = clean(input.subject);
  const chapter = clean(input.chapter);
  const slots = Array.isArray(input.slots) ? [...new Set(input.slots.filter(s => typeof s === "string"))] : [];

  if (!/^[\p{L}][\p{L} '\-]{0,29}$/u.test(firstName)) return { ok: false, error: "Please enter your first name (letters only, up to 30)." };
  if (className.length < 1 || className.length > 12) return { ok: false, error: "Please enter your class (up to 12 characters)." };
  if (!SUBJECTS.includes(subject)) return { ok: false, error: "Please choose a subject from the list." };
  if (chapter.length < 1 || chapter.length > 40) return { ok: false, error: "Please enter the chapter (up to 40 characters)." };
  if (slots.length < 1) return { ok: false, error: "Please tick at least one free time." };
  if (!slots.every(s => SLOTS.includes(s))) return { ok: false, error: "Unknown time slot." };

  // Keep slots in the calendar order, so matching is predictable.
  const ordered = SLOTS.filter(s => slots.includes(s));
  return { ok: true, value: { firstName, className, subject, chapter: chapter.toLowerCase(), slots: ordered } };
}

// Choose an existing group for a student, or null if a new group is needed.
// groups: [{ id, slot, members }] that already share the student's subject and chapter.
// Prefers the earliest shared time, then the fullest group (so groups fill up and actually meet).
export function chooseGroup(groups, slots, max = MAX_GROUP) {
  const open = groups.filter(g => g.members < max && slots.includes(g.slot));
  if (!open.length) return null;
  open.sort((a, b) => SLOTS.indexOf(a.slot) - SLOTS.indexOf(b.slot) || b.members - a.members);
  return open[0];
}

// Time slot for a brand-new group: the student's earliest free time.
export function newGroupSlot(slots) {
  return SLOTS.find(s => slots.includes(s)) ?? null;
}
