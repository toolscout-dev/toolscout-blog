# PROHIBITED.md — Comandi Vietati

## ⚠️ MAI ESEGUIRE QUESTI COMANDI

### 1. `openclaw gateway restart`
**Perché vietato:** Interrompe tutti gli agent e le sessioni attive. Può causare perdita di dati o stato.

**Alternativa:** Se necessario, chiedere sempre a Michael prima.

### 2. Modifiche a `openclaw.json`
**Perché vietato:** File di configurazione core di OpenClaw. Errori qui possono disabilitare l'intero sistema.

**Alternativa:** Usare file di configurazione nel workspace (`.openclaw/heartbeat.json`, etc.)

### 3. Altri comandi riservati
- `openclaw gateway stop` (senza esplicito permesso)
- `openclaw configure` (modifica config globale)
- Qualsiasi modifica ai file in `~/.openclaw/` tranne workspace

## ✅ Approccio Corretto
Per configurare automazioni, usare:
- File nel workspace (`.openclaw/`, `HEARTBEAT.md`, etc.)
- Comandi agent-specifici
- Task scheduler di sistema (se necessario)
