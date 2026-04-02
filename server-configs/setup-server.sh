#!/bin/bash
# ─────────────────────────────────────────────────────────
# EC2 Server Setup Script
# Run this ONCE on a fresh Ubuntu 24.04 EC2 instance.
# Usage: ssh into your server, then:
#   chmod +x setup-server.sh
#   ./setup-server.sh
# ─────────────────────────────────────────────────────────

set -e  # Stop on any error

echo "══════════════════════════════════════════"
echo "  Step 1/6: System packages"
echo "══════════════════════════════════════════"
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-venv python3-pip \
    nginx certbot python3-certbot-nginx \
    git libpq-dev

echo "══════════════════════════════════════════"
echo "  Step 2/6: Clone the repo"
echo "══════════════════════════════════════════"
cd /home/ubuntu
if [ ! -d "dogwood-backend" ]; then
    git clone git@github.com:YOUR-ORG/dogwood-backend.git
fi
cd dogwood-backend

echo "══════════════════════════════════════════"
echo "  Step 3/6: Python virtual environment"
echo "══════════════════════════════════════════"
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements/prod.txt

echo "══════════════════════════════════════════"
echo "  Step 4/6: Environment file"
echo "══════════════════════════════════════════"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "  ⚠️  IMPORTANT: Edit /home/ubuntu/dogwood-backend/.env"
    echo "     Fill in your real database credentials and secret key."
    echo "     Run: nano /home/ubuntu/dogwood-backend/.env"
    echo ""
fi

echo "══════════════════════════════════════════"
echo "  Step 5/6: Gunicorn service"
echo "══════════════════════════════════════════"
sudo cp /home/ubuntu/dogwood-backend/server-configs/gunicorn.service \
    /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn

echo "══════════════════════════════════════════"
echo "  Step 6/6: Nginx"
echo "══════════════════════════════════════════"
sudo cp /home/ubuntu/dogwood-backend/server-configs/nginx-dogwood.conf \
    /etc/nginx/sites-available/dogwood
sudo ln -sf /etc/nginx/sites-available/dogwood /etc/nginx/sites-enabled/dogwood
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t

echo ""
echo "══════════════════════════════════════════"
echo "  DONE! Next steps:"
echo "══════════════════════════════════════════"
echo ""
echo "  1. Edit your .env file:"
echo "     nano /home/ubuntu/dogwood-backend/.env"
echo ""
echo "  2. Run database migrations:"
echo "     cd /home/ubuntu/dogwood-backend"
echo "     source venv/bin/activate"
echo "     python manage.py migrate"
echo "     python manage.py createsuperuser"
echo ""
echo "  3. Get your SSL certificate:"
echo "     sudo certbot --nginx -d your-domain.com -d www.your-domain.com"
echo ""
echo "  4. Start everything:"
echo "     sudo systemctl start gunicorn"
echo "     sudo systemctl restart nginx"
echo ""
