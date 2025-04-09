# 🥬 Lettuce

**Lettuce** is a lightweight, YAML-configurable wrapper for `rsync`, designed to keep your local project folder in sync with a remote target (like a Docker server or homelab).

It's inspired by tools like [Mutagen](https://mutagen.io/), but without the agent complexity or platform limitations — perfect for lightweight dev flows from environments like Termux.

---

## 🚀 Features

- 🧠 Simple YAML config (`lettuce.yml`)
- 🚀 Fast file sync with `rsync`
- 🧹 Ignores and allows files with glob patterns
- 👀 Optional `watch` mode to sync on file change
- 🥗 Lightweight, zero-daemon, no magic

---

## 📦 Installation

**Install directly from GitHub:**

```bash
pip install git+https://github.com/cr8ivecodesmith/lettuce.git
```

**Or clone and install locally for development:**

```bash
git clone https://github.com/cr8ivecodesmith/lettuce.git
cd lettuce
pip install -e .
```

**Make sure you have:**

- Python 3.7+
- `rsync` installed and accessible
- `watchdog` if you want to use `lettuce watch`

---

## 📁 Example `lettuce.yml`

```yaml
source: .
target: user@192.168.1.2:/srv/projects/myproject

ignore:
  - ".git/"
  - "*.pyc"
  - "__pycache__/"
  - "lettuce.yml"

# Optional allow list:
# allow:
#   - "src/**"
#   - "Makefile"
```

---

## 🧪 Usage

### One-time sync:

```bash
lettuce sync
```

### Watch and sync on file change:

```bash
lettuce watch
```

### Use a different config file:

```bash
lettuce sync --config custom.yml
```

---

## 🛠 How it Works

Lettuce wraps `rsync` with options derived from your YAML config:
- `--exclude` for ignore patterns
- `--include` and fallback `--exclude=*` for allowlist
- Uses `rsync -avz --delete` by default

---

## 📌 Why Lettuce?

Lettuce is built for people who:
- Want to code in Termux or remote-first setups
- Use a homelab or external Docker host
- Don’t want to fight with agent binaries or kernel syscall issues

---

## 📚 License

MIT © Matt Lebrun <matt@lebrun.org>

---

> 🥬 Lettuce sync, so you don’t have to think.™

