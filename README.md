<p align="center">
  <img src="https://i.ibb.co/fzCpHbKs/x.jpg" alt="Shadowd TombBotz Logo">
</p>
<h1 align="center">
  SHADOWD TOMBBOTZ - Advanced Filter Bot
</h1>

![Typing SVG](https://readme-typing-svg.herokuapp.com/?lines=Welcome+To+Shadowd+TombBotz!;Advanced+Telegram+Filter+Bot;Optimized+For+Performance!)
</p>

<p align="center">
  <a href="https://t.me/shadowedtomb">
    <img src="https://img.shields.io/badge/Telegram-Channel-blue?style=for-the-badge&logo=telegram" alt="Telegram Channel">
  </a>
  <a href="https://t.me/shadowedtomb_discussion">
    <img src="https://img.shields.io/badge/Telegram-Support-blue?style=for-the-badge&logo=telegram" alt="Support Group">
  </a>
  <a href="https://github.com/VJBots/VJ-Filter-Bot">
    <img src="https://img.shields.io/github/stars/VJBots/VJ-Filter-Bot?style=for-the-badge" alt="GitHub Stars">
  </a>
</p>

---

## 🚀 Main Features 

<b>

### Core Features
- [x] **Multiple Database Support** - Unlimited MongoDB connections with dynamic management
- [x] **Advanced Caching System** - In-memory caching with TTL for faster responses
- [x] **Database Health Monitoring** - Real-time connection health checks
- [x] **Query Optimization** - Intelligent query routing and load balancing
- [x] **AI Spell Check** - Smart search with typo correction
- [x] **Custom Force Subscribe** - Flexible force subscribe with request-to-join support
- [x] **Rename Feature** - File renaming with custom captions and thumbnails
- [x] **Stream Feature** - Multiple player support for streaming
- [x] **PM Search** - Private message search capability
- [x] **Auto Approve** - Automatic join request approval
- [x] **Send All Button** - Batch file sending
- [x] **Auto Delete** - Automatic message cleanup

### Advanced Features
- [x] **Platform Detection** - Auto-detects Heroku, Koyeb, and Render
- [x] **Keep-Alive System** - Prevents service sleep on all platforms
- [x] **UI Renderer** - Beautiful search results formatting
- [x] **Text Formatter** - Unicode small caps and markdown support
- [x] **Admin Commands** - Comprehensive database and cache management
- [x] **Language/Season/Quality Filters** - Advanced content filtering
- [x] **Global Filters** - Bot-wide filter management
- [x] **Batch Link Generation** - Create shareable links for multiple files

**Note**: You can turn on or off every feature. Just use which feature you want by enabling it in settings.

</b>

---

## 📋 Commands

<details>
<summary><b>👤 User Commands</b></summary>

```
• /start - Start the bot
• /search - Search from various sources
• /info - Get user information
• /id - Get Telegram IDs
• /imdb - Fetch info from IMDb
• /stream - Generate stream and download link
• /telegraph - Get telegraph link (files under 5MB)
• /stickerid - Get sticker ID
• /font - Get different font styles
• /repo - Search GitHub repositories
```
</details>

<details>
<summary><b>👑 Admin Commands</b></summary>

```
• /index - Index files from your channel
• /setskip - Skip messages when indexing
• /logs - Get recent error logs
• /stats - Get database statistics
• /connections - See all connected groups
• /settings - Open settings menu
• /users - Get list of users
• /chats - Get list of chats
• /leave - Leave from a chat
• /disable - Disable a chat
• /enable - Re-enable a chat
• /ban - Ban a user
• /unban - Unban a user
• /channel - List connected channels
• /broadcast - Broadcast to all users
• /grp_broadcast - Broadcast to all groups
• /restart - Restart the bot
• /deleteall - Delete all indexed files
• /delete - Delete specific file
• /deletefiles - Delete PreDVD and CamRip files
• /purgerequests - Delete all join requests
• /totalrequests - Get total join requests
```
</details>

<details>
<summary><b>🔧 Filter Commands</b></summary>

```
• /filter - Add manual filters
• /filters - View filters
• /del - Delete a filter
• /delall - Delete all filters
• /gfilter - Add global filters
• /gfilters - View global filters
• /delg - Delete a global filter
• /delallg - Delete all global filters
```
</details>

<details>
<summary><b>🔗 Connection Commands</b></summary>

```
• /connect - Connect to PM
• /disconnect - Disconnect from PM
• /fsub - Add force subscribe channel
• /nofsub - Remove force subscribe
```
</details>

<details>
<summary><b>📝 Rename Commands</b></summary>

```
• /rename - Rename your file
• /set_caption - Add caption for renamed file
• /see_caption - See your saved caption
• /del_caption - Delete your saved caption
• /set_thumb - Add thumbnail for renamed file
• /view_thumb - View your saved thumbnail
• /del_thumb - Delete your saved thumbnail
```
</details>

<details>
<summary><b>🔗 Batch Commands</b></summary>

```
• /batch - Create link for multiple posts
• /link - Create link for one post
```
</details>

<details>
<summary><b>⚙️ Database Management Commands (Admin)</b></summary>

```
• /dbstats - Get database statistics
• /adddb - Add new database connection
• /removedb - Remove database connection
• /listdbs - List all database connections
• /dbhealth - Check database health status
• /cachestats - Get cache statistics
• /clearcache - Clear all cache
```
</details>

---

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Get from [@BotFather](https://t.me/BotFather) | `1234567890:ABCdefGHI...` |
| `API_ID` | Get from [my.telegram.org](https://my.telegram.org/apps) | `12345678` |
| `API_HASH` | Get from [my.telegram.org](https://my.telegram.org/apps) | `abcdef1234567890...` |
| `DATABASE_URI` | MongoDB connection string | `mongodb+srv://user:pass@...` |
| `LOG_CHANNEL` | Channel ID for logging | `-1001234567890` |
| `CHANNELS` | File channel IDs (space-separated) | `-1001234567890 -1009876543210` |
| `ADMINS` | Admin user IDs (space-separated) | `123456789 987654321` |

### Optional Variables

<details>
<summary><b>Click to expand optional variables</b></summary>

| Variable | Description | Default |
|----------|-------------|---------|
| `SESSION` | Bot session name | `ShadowedTombbotz` |
| `DATABASE_NAME` | MongoDB database name | `shadowedtombbotz` |
| `COLLECTION_NAME` | MongoDB collection name | `shadowedtombcollection` |
| `AUTH_CHANNEL` | Force subscribe channel ID | None |
| `SUPPORT_CHAT_ID` | Support group ID | None |
| `REQST_CHANNEL` | Request channel ID | None |
| `PORT` | Web server port | `8080` |
| `URL` | Your deployment URL | Required for Render/Koyeb |
| `STREAM_MODE` | Enable streaming | `True` |
| `RENAME_MODE` | Enable rename feature | `False` |
| `AUTO_APPROVE_MODE` | Auto approve join requests | `False` |
| `IMDB` | Enable IMDb integration | `False` |
| `AUTO_DELETE` | Auto delete messages | `True` |
| `PROTECT_CONTENT` | Protect content from forwarding | `False` |
| `AI_SPELL_CHECK` | Enable AI spell check | `True` |
| `PM_SEARCH` | Enable PM search | `True` |
| `MULTIPLE_DATABASE` | Enable multiple databases | `False` |
| `DYNAMIC_DB_MODE` | Enable dynamic DB management | `False` |

</details>

---

## 🚀 Deployment Options

### Deploy to Render (Recommended) ⭐

<details>
<summary><b>Click for Render deployment instructions</b></summary>

#### Quick Deploy (5 Minutes)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Create Render Service**
   - Go to [Render.com](https://render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Environment**: Docker
     - **Dockerfile Path**: `VJ-FILTER-BOT-Tech_VJ/Dockerfile`
     - **Region**: Choose closest to your users

3. **Set Environment Variables**
   - Add all required variables from the table above
   - **Important**: Set `URL` to your Render app URL

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build
   - Check logs for "Bot Restarted" message

#### Detailed Guide
See [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for comprehensive instructions.

#### Quick Reference
See [QUICK_DEPLOY_RENDER.md](../QUICK_DEPLOY_RENDER.md) for 5-minute quick start.

</details>

---

### Deploy to Koyeb

<details>
<summary><b>Click for Koyeb deployment instructions</b></summary>

#### Quick Deploy

1. **Push to GitHub** (same as Render)

2. **Create Koyeb Service**
   - Go to [Koyeb.com](https://www.koyeb.com/)
   - Click "Create Service"
   - Select "Docker" deployment
   - Connect your GitHub repository
   - Configure:
     - **Dockerfile Path**: `VJ-FILTER-BOT-Tech_VJ/Dockerfile`
     - **Port**: `8080`

3. **Set Environment Variables**
   - Add all required variables
   - **Important**: Set `URL` to your Koyeb app URL

4. **Deploy**
   - Click "Deploy"
   - Wait 5-10 minutes
   - Check logs for "Bot Restarted"

#### Detailed Guide
See [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for comprehensive instructions.

</details>

---

### Deploy to Heroku

<details>
<summary><b>Click for Heroku deployment instructions</b></summary>

1. **Connect GitHub Account**
   - Go to Heroku Dashboard
   - Create new app
   - Connect to GitHub repository

2. **Configure**
   - Select repository and branch
   - Enable automatic deploys (optional)

3. **Set Environment Variables**
   - Go to Settings → Config Vars
   - Add all required variables

4. **Deploy**
   - Click "Deploy Branch"
   - Wait for build to complete

**Note**: Heroku free tier has been discontinued. Consider using Render or Koyeb instead.

</details>

---

### Deploy to VPS

<details>
<summary><b>Click for VPS deployment instructions</b></summary>

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd https://github.com/arkiyaalya/filterauto

# Install dependencies
pip3 install -U -r requirements.txt

# Edit info.py with your variables
nano info.py

# Run bot
python3 bot.py
```

#### Using Docker (Recommended)

```bash
# Build Docker image
docker build -t shadowd-tombbotz .

# Run container
docker run -d --name shadowd-bot \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e BOT_TOKEN=your_bot_token \
  -e DATABASE_URI=your_mongodb_uri \
  -e LOG_CHANNEL=your_log_channel \
  -e CHANNELS=your_channels \
  -e ADMINS=your_admins \
  shadowd-tombbotz
```

#### Using PM2 (Process Manager)

```bash
# Install PM2
npm install -g pm2

# Start bot with PM2
pm2 start bot.py --name shadowd-bot --interpreter python3

# Save PM2 configuration
pm2 save

# Enable PM2 startup
pm2 startup
```

</details>

---

## 📊 Performance Optimizations

This bot includes several performance optimizations:

### 🚀 Caching System
- In-memory caching with TTL (Time To Live)
- Caches search results, user settings, and file metadata
- Reduces database load by up to 70%
- Configurable cache expiration times

### 💾 Database Management
- Dynamic database connection pooling
- Automatic failover and load balancing
- Health monitoring with automatic recovery
- Support for unlimited MongoDB connections
- Query optimization and intelligent routing

### 🎨 UI Enhancements
- Beautiful search results formatting
- Unicode small caps text rendering
- Markdown formatting support
- Responsive button layouts

### ⚡ Query Optimization
- Intelligent query routing
- Connection pooling
- Automatic retry with exponential backoff
- Load balancing across multiple databases

---

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)** - Complete deployment guide for Koyeb & Render
- **[QUICK_DEPLOY_RENDER.md](../QUICK_DEPLOY_RENDER.md)** - 5-minute quick start for Render
- **[RENDER_DEPLOYMENT_CHECKLIST.md](../RENDER_DEPLOYMENT_CHECKLIST.md)** - Pre-deployment verification
- **[KOYEB_RENDER_UPDATES.md](../KOYEB_RENDER_UPDATES.md)** - Platform compatibility updates

---

## 🛠️ Troubleshooting

<details>
<summary><b>Common Issues and Solutions</b></summary>

### Bot Not Starting
- ✅ Verify all required environment variables are set
- ✅ Check MongoDB connection string is correct
- ✅ Ensure BOT_TOKEN is valid
- ✅ Review deployment logs for error messages

### Database Connection Failed
- ✅ Verify MongoDB Atlas IP whitelist (allow 0.0.0.0/0)
- ✅ Check database user has read/write permissions
- ✅ Test connection string using MongoDB Compass

### Import Errors
- ✅ Ensure all dependencies in requirements.txt
- ✅ Check HailArka folder exists in repository
- ✅ Verify Python version is 3.10.8

### Bot Goes Offline (Render Free Tier)
- ✅ Render free tier spins down after 15 min inactivity
- ✅ Use external keep-alive service (UptimeRobot)
- ✅ Upgrade to paid plan for 24/7 uptime

### Module Not Found
- ✅ Reinstall dependencies: `pip3 install -U -r requirements.txt`
- ✅ Check all files are present in repository
- ✅ Verify folder structure is intact

</details>

---

## 🔄 Updates & Maintenance

### Recent Updates
- ✅ Added Render and Koyeb platform support
- ✅ Implemented advanced caching system
- ✅ Added database health monitoring
- ✅ Improved query optimization
- ✅ Enhanced UI rendering
- ✅ Added dynamic database management
- ✅ Implemented keep-alive for all platforms

### Updating Your Bot

#### Via Git Pull
```bash
cd https://github.com/arkiyaalya/filterauto
git pull origin main
pip3 install -U -r requirements.txt
python3 bot.py
```

#### Via Render/Koyeb
- Push changes to GitHub
- Platforms will auto-deploy

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 💬 Support

Need help? Join our community:

- **Telegram Channel**: [@shadowedtomb](https://t.me/shadowedtomb)
- **Support Group**: [@shadowedtomb_discussion](https://t.me/shadowedtomb_discussion)
- **Developer**: [@Hail_Arka](https://t.me/Hail_Arka)
- **Maintainer**: [@Shadowedtomb](https://t.me/Shadowedtomb)

---

## 🙏 Credits

- **Base Repository**: [Eva Marie](https://t.me/TeamEvamaria)
- **Pyrogram Library**: [Pyrogram](https://github.com/pyrogram/pyrogram)
- **Pyrofork Library**: [Pyrofork](https://github.com/Mayuri-Chan/pyrofork)
- **Modified & Maintained by**: [@Shadowedtomb](https://t.me/Shadowedtomb) and [@Hail_Arka](https://t.me/Hail_Arka)

---

## ⚖️ License

[![GNU Affero General Public License 2.0](https://www.gnu.org/graphics/agplv3-155x51.png)](https://www.gnu.org/licenses/agpl-3.0.en.html#header)

Licensed under [GNU AGPL 2.0](LICENSE)

**⚠️ Important**: Selling the codes to other people for money is **strictly prohibited**.

---

## 📝 Note

- Fork the repo and edit as per your needs
- For support or questions, contact [@Shadowedtomb](https://t.me/Shadowedtomb) or [@Hail_Arka](https://t.me/Hail_Arka)
- Star ⭐ the repository if you find it useful!

---

<p align="center">
  <b>Made with ❤️ by Shadowd TombBotz Team</b>
</p>

<p align="center">
  <a href="https://t.me/shadowedtomb">
    <img src="https://img.shields.io/badge/Join-Telegram%20Channel-blue?style=for-the-badge&logo=telegram" alt="Telegram Channel">
  </a>
</p>
