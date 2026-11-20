# Verify SSL Certificates

Can turn off SSL certificate verification on a task. Useful if you have e.g. an https <plugin:rss> input which does not have a valid certificate.
```yaml
verify_ssl_certificates: no
```

**`WARNING:`** Make sure you understand the risks before disabling SSL certificate verification on a task. This plugin will affect every HTTPS network request in that task.