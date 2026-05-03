# Hardening minimo de host

## Usuario de deploy sem root

```bash
sudo adduser --disabled-password --gecos "" deploy
sudo usermod -aG docker deploy
```

## SSH restrito

- Permitir apenas chave publica.
- Desabilitar login por senha em `/etc/ssh/sshd_config`.
- Restringir porta 22 a seu IP no Security Group.

## Fail2ban (opcional)

```bash
sudo apt-get update
sudo apt-get install -y fail2ban
sudo systemctl enable --now fail2ban
```

## Logrotate para logs Docker

Adicione em `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Reinicie Docker:

```bash
sudo systemctl restart docker
```

## Backups RDS

- Configure `backup-retention-period >= 7`.
- Habilite snapshots manuais antes de mudanças criticas.
