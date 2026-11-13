/* SafeNight data adapter -- THE SWAP POINT for integration.
 *
 * The UI only talks to the functions in this file. Right now they return placeholder
 * data. At integration, the routing and hazard services replace the bodies while
 * keeping the same return shapes. Nothing else in the UI needs to change.
 *
 * Route contract (plus OPTIONAL geometry for the map):
 *   {
 *     shortest:   { distance_m: 850,  risk_indicator: 0.42, path: [[lat, lon], ...], segment_risk: [0.3, ...] },
 *     lower_risk: { distance_m: 1100, risk_indicator: 0.25, path: [...],              segment_risk: [...] }
 *   }
 *   risk_indicator === null  -> the UI shows a "Data limited" state.
 *   getRouteResult() resolves to null -> the UI shows a "No route found" state.
 *
 * All values below are illustrative placeholders, not verified SafeNight predictions.
 */
(function () {
  'use strict';
  const SN = (window.SN = window.SN || {});

  const HAZARD_TYPES = ['broken_streetlight', 'dark_path', 'blocked_footpath', 'other_infrastructure'];
  const HAZARD_LABELS = {
    broken_streetlight: 'Broken streetlight',
    dark_path: 'Dark path',
    blocked_footpath: 'Blocked footpath',
    other_infrastructure: 'Other infrastructure issue',
  };
  const WALK_KMH = 5; // shown to the user; used for the walking-time estimate

  const START = { lat: 12.934, lon: 77.618, name: 'Start' };
  const END = { lat: 12.9353, lon: 77.6258, name: 'End' };

  const SHORT_PATH = [[12.934, 77.618], [12.9342, 77.6192], [12.9345, 77.6204], [12.9347, 77.6216],
    [12.9348, 77.6228], [12.935, 77.624], [12.9352, 77.625], [12.9353, 77.6258]];
  const LOW_PATH = [[12.934, 77.618], [12.9333, 77.6185], [12.9325, 77.6192], [12.9318, 77.6201],
    [12.9314, 77.6212], [12.9314, 77.6224], [12.9318, 77.6235], [12.9327, 77.6244],
    [12.9338, 77.6251], [12.9347, 77.6255], [12.9353, 77.6258]];
  const SHORT_SEG = [0.3, 0.35, 0.55, 0.62, 0.58, 0.45, 0.4, 0.38, 0.35, 0.3, 0.28, 0.3];
  const LOW_SEG = [0.2, 0.18, 0.22, 0.25, 0.3, 0.28, 0.24, 0.22, 0.26, 0.27, 0.25, 0.22];

  const BASE_HAZARDS = [
    { lat: 12.9347, lon: 77.6214, label: 'Broken streetlight', status: 'confirmed' },
    { lat: 12.9362, lon: 77.6226, label: 'Dark path', status: 'new' },
  ];

  const ATLAS_BOUNDS = { south: 12.9275, north: 12.9395, west: 77.6145, east: 77.6295, cols: 20, rows: 12 };

  const clone = (o) => JSON.parse(JSON.stringify(o));
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));

  // Placeholder store: reports live in this browser tab only.
  const hazards = clone(BASE_HAZARDS);

  /** SWAP POINT (routing). state: 'normal' | 'limited' | 'no_route' (preview switch only). */
  async function getRouteResult(state = 'normal', source = '', dest = '') {
    await wait(650); // placeholder latency so the loading state is visible
    if (state === 'no_route') return null;
    let short = { distance_m: 850, risk_indicator: 0.42, path: SHORT_PATH, segment_risk: SHORT_SEG };
    let low = { distance_m: 1100, risk_indicator: 0.25, path: LOW_PATH, segment_risk: LOW_SEG };
    if (state === 'limited') {
      short = Object.assign({}, short, { risk_indicator: null, segment_risk: null });
      low = Object.assign({}, low, { risk_indicator: null, segment_risk: null });
    }
    return clone({ shortest: short, lower_risk: low });
  }

  /** SWAP POINT (hazards: get_active_hazards). */
  function getHazards() {
    return hazards;
  }

  /** SWAP POINT (hazards: add_hazard). Resolves to { ok, message }. Placeholder: nothing is saved. */
  async function submitHazard(lat, lon, hazardType, description = '') {
    await wait(350);
    if (!HAZARD_TYPES.includes(hazardType)) return { ok: false, message: 'Pick a hazard category.' };
    if (!(Number.isFinite(lat) && Number.isFinite(lon) && lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180)) {
      return { ok: false, message: 'Location is out of range. Latitude must be -90 to 90 and longitude -180 to 180.' };
    }
    if (description.length > 200) return { ok: false, message: 'Description is too long (200 characters max).' };
    const h = { lat, lon, label: HAZARD_LABELS[hazardType], status: 'new', description, ts: Date.now() };
    hazards.push(h);
    return {
      ok: true,
      hazard: h,
      message: `Report received: ${HAZARD_LABELS[hazardType]}. It starts as unverified. Demo only, nothing is saved yet.`,
    };
  }

  /* ---------- Accounts: SWAP POINT (auth service) ----------
   * Placeholder: the profile lives in this browser's localStorage. Passwords are checked for
   * shape only and never stored. A real backend replaces these bodies, keeping the shapes:
   *   profile = { name, email, phone, gender, dob, memberSince, contacts: [{ name, phone }], beta }
   */
  const PKEY = 'sn.profile';
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  function readProfile() {
    try { const p = JSON.parse(localStorage.getItem(PKEY)); return p && typeof p === 'object' ? p : null; } catch (_) { return null; }
  }
  function writeProfile(p) {
    try { if (p) localStorage.setItem(PKEY, JSON.stringify(p)); else localStorage.removeItem(PKEY); } catch (_) { /* storage unavailable */ }
    return p;
  }
  const nameFromEmail = (e) => e.split('@')[0].replace(/[._-]+/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  const GENDERS = ['Female', 'Male', 'Non-binary', 'Prefer not to say'];
  const PHONE_RE = /^\+?[\d\s()-]{7,}$/;
  const thisMonth = () => new Date().toISOString().slice(0, 7); // "YYYY-MM"
  const blank = (extra) => Object.assign({ name: '', email: '', phone: '', gender: '', dob: '', contacts: [], beta: 2, memberSince: thisMonth() }, extra);

  /** Field rules shared by sign-up and profile edits. Returns an error message or ''. */
  function checkField(k, v) {
    v = (v || '').trim();
    if (k === 'name') return v ? (v.length > 60 ? 'Name is too long (60 characters max).' : '') : 'Enter your name.';
    if (k === 'email') return EMAIL_RE.test(v) ? '' : 'Enter a valid email address.';
    if (k === 'phone') return PHONE_RE.test(v) && v.replace(/\D/g, '').length >= 7 ? '' : 'Enter a valid phone number, e.g. +91 98765 43210.';
    if (k === 'gender') return !v || GENDERS.includes(v) ? '' : 'Pick an option from the list.';
    if (k === 'dob') {
      if (!v) return '';
      const d = new Date(v + 'T00:00:00');
      if (isNaN(d)) return 'Enter a valid date.';
      if (d > new Date()) return 'Date of birth can’t be in the future.';
      if (d.getFullYear() < 1900) return 'Enter a year after 1900.';
      return '';
    }
    return '';
  }

  const auth = {
    GENDERS,
    checkField,
    current() {
      const p = readProfile();
      if (p && p.guest) { writeProfile(null); return null; } // guest sessions are no longer supported
      if (p && !p.memberSince) { p.memberSince = thisMonth(); writeProfile(p); }
      return p;
    },
    async signIn(email, password) {
      await wait(500);
      email = (email || '').trim().toLowerCase();
      if (!EMAIL_RE.test(email)) return { ok: false, message: 'Enter a valid email address.' };
      if (!password) return { ok: false, message: 'Enter your password.' };
      const prev = readProfile();
      const p = prev && prev.email === email ? prev : blank({ name: nameFromEmail(email), email });
      return { ok: true, profile: writeProfile(p) };
    },
    /** extra = { phone, gender, dob } */
    async signUp(name, email, password, extra = {}) {
      await wait(600);
      name = (name || '').trim(); email = (email || '').trim().toLowerCase();
      const phone = (extra.phone || '').trim(), gender = extra.gender || '', dob = extra.dob || '';
      const err = checkField('name', name) || checkField('email', email) ||
        ((password || '').length < 8 ? 'Use a password with at least 8 characters.' : '') ||
        checkField('phone', phone) || checkField('gender', gender) || checkField('dob', dob);
      if (err) return { ok: false, message: err };
      return { ok: true, profile: writeProfile(blank({ name, email, phone, gender, dob })) };
    },
    /** Update one or more personal fields. Resolves to { ok, message?, profile? }. */
    async update(fields) {
      await wait(250);
      const p = readProfile();
      if (!p) return { ok: false, message: 'You are signed out.' };
      for (const k of Object.keys(fields)) {
        const v = (fields[k] || '').trim();
        const err = checkField(k, v);
        if (err) return { ok: false, message: err };
        p[k] = k === 'email' ? v.toLowerCase() : v;
      }
      return { ok: true, profile: writeProfile(p) };
    },
    async save(p) { return writeProfile(p); },
    async signOut() { writeProfile(null); return { ok: true }; },
  };

  SN.data = {
    HAZARD_TYPES, HAZARD_LABELS, WALK_KMH, START, END, BASE_HAZARDS, ATLAS_BOUNDS,
    getRouteResult, getHazards, submitHazard, clone, auth,
  };
})();
