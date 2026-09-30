// Unit tests for matching and input checks. Run with: npm test  (uses Node's built-in test runner, no install needed)
import { test } from "node:test";
import assert from "node:assert/strict";
import { validateSignup, chooseGroup, newGroupSlot, MAX_GROUP } from "../src/match.js";

const mia = { firstName: "Mia", className: "10B", subject: "Math", chapter: "Chapter 3", slots: ["Thu 4 pm", "Tue 4 pm"] };

test("a normal sign-up is accepted and cleaned", () => {
  const r = validateSignup({ ...mia, firstName: "  Mia  " });
  assert.equal(r.ok, true);
  assert.equal(r.value.firstName, "Mia");
  assert.equal(r.value.chapter, "chapter 3");                 // chapters compare case-insensitively
  assert.deepEqual(r.value.slots, ["Tue 4 pm", "Thu 4 pm"]);  // calendar order
});

test("edge: empty name is rejected", () => {
  assert.equal(validateSignup({ ...mia, firstName: "" }).ok, false);
});

test("edge: very long name is rejected", () => {
  assert.equal(validateSignup({ ...mia, firstName: "A".repeat(500) }).ok, false);
});

test("edge: a script in the name is rejected", () => {
  assert.equal(validateSignup({ ...mia, firstName: "<script>steal()</script>" }).ok, false);
});

test("edge: unknown subject or time slot is rejected", () => {
  assert.equal(validateSignup({ ...mia, subject: "Hacking" }).ok, false);
  assert.equal(validateSignup({ ...mia, slots: ["Mon 3 am"] }).ok, false);
  assert.equal(validateSignup({ ...mia, slots: [] }).ok, false);
});

test("Mia joins an open Tuesday group", () => {
  const groups = [{ id: "a", slot: "Tue 4 pm", members: 2 }, { id: "b", slot: "Fri 4 pm", members: 1 }];
  assert.equal(chooseGroup(groups, ["Tue 4 pm", "Thu 4 pm"]).id, "a");
});

test("a full group is skipped", () => {
  const groups = [{ id: "full", slot: "Tue 4 pm", members: MAX_GROUP }, { id: "open", slot: "Thu 4 pm", members: 1 }];
  assert.equal(chooseGroup(groups, ["Tue 4 pm", "Thu 4 pm"]).id, "open");
});

test("no shared time means a new group", () => {
  const groups = [{ id: "a", slot: "Mon 4 pm", members: 1 }];
  assert.equal(chooseGroup(groups, ["Sat 10 am"]), null);
  assert.equal(newGroupSlot(["Sun 10 am", "Sat 10 am"]), "Sat 10 am");
});

test("earliest shared time wins, then the fuller group", () => {
  const groups = [{ id: "thu", slot: "Thu 4 pm", members: 3 }, { id: "tue1", slot: "Tue 4 pm", members: 1 }, { id: "tue2", slot: "Tue 4 pm", members: 3 }];
  assert.equal(chooseGroup(groups, ["Tue 4 pm", "Thu 4 pm"]).id, "tue2");
});

test("edge: two hundred students at once still make groups of at most four", () => {
  const groups = [];
  for (let i = 0; i < 200; i++) {
    const slots = [["Mon 4 pm", "Tue 4 pm", "Wed 4 pm"][i % 3]];
    let g = chooseGroup(groups, slots);
    if (!g) { g = { id: `g${groups.length}`, slot: newGroupSlot(slots), members: 0 }; groups.push(g); }
    g.members++;
  }
  assert.ok(groups.every(g => g.members <= MAX_GROUP));
  assert.equal(groups.reduce((n, g) => n + g.members, 0), 200);
});
