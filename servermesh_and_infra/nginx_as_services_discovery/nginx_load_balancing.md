### HTTP Load Balancing

```nginx
http {
    upstream my_upstream {
        server server1.example.com;
        server server2.example.com;
    }

    server {
        listen 80;
        location / {
            proxy_set_header Host $host;
            proxy_pass http://my_upstream;
        }
    }
}
```

---

### TCP and UDP Load Balancing

```nginx
stream {
    upstream my_upstream {
        server server1.example.com:1234;
        server server2.example.com:2345;
    }

    server {
        listen 1123 [udp];
        proxy_pass my_upstream;
    }
}
```

---

### Session 持久化

```nginx
upstream backend {
    server webserver1;
    server webserver2;

    sticky cookie srv_id expires=1h domain=.example.com path=/;
}
`https://cdn-1.wp.nginx.com/wp-content/uploads/2016/04/Richardson-microservices-part4-1_difficult-service-discovery.pngtream my_upstream {
zone my_upstream 64k;
server server1.example.com slow_start=30s;
}

server {
# ...
    location /health {
        internal;
        health_check interval=5s uri=/test.php match=statusok;
        proxy_set_header HOST www.example.com;
        proxy_pass http://my_upstream
    }
}

match statusok {
# Used for /test.php health check
    status 200;
    header Content-Type = text/html;
    body ~ "Server[0-9]+ is alive";
}
```

---

### 使用 DNS 做服务发现

```nginx
resolver 127.0.0.11 valid=10s;

upstream service1 {
    zone service1 64k;
    server service1 service=http resolve;
}
```

