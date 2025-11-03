# Propuesta profesional: Plataforma IA para salud dental (web + CRM/ERP)



## 1) Resumen ejecutivo (Elevator pitch)

**DentAI Track** es una plataforma web que permite a usuarios **monitorear su salud bucal** con ayuda de IA. La aplicación facilita:

* Registro e inicio de sesión seguro.
* Captura/subida de fotos intraorales.
* Detección automática de **caries, gingivitis y placa** (extensible a otras afecciones: lesiones, cálculo, recesión, etc.).
* **Historial longitudinal** con comparativas y gráficas de evolución.
* **Recordatorios** de higiene, controles y citas.
* Módulo **CRM** opcional para clínicas (seguimiento de pacientes, campañas de prevención) y **ERP** opcional (turnos, insumos, facturación).

**Rol de la IA:** modelado de clasificación/detección multi‑etiqueta, inferencia en tiempo real, y explicabilidad por mapas de calor.

**Diferenciador:** foco en **usabilidad**, **privacidad** y **valor clínico** con métricas claras (sensibilidad por clase, tasa de falsos negativos) y pipeline MLOps reproducible.

---

## 2) Objetivos

1. **MVP (8–10 semanas):**

   * Autenticación/registro, perfiles, carga/captura de imágenes.
   * Inferencia IA para **caries** y **gingivitis** + etiqueta **“sin hallazgos”**.
   * Registro histórico y dashboard de evolución.
   * Exportación de reporte PDF con recomendaciones generales (no diagnóstico).
2. **Versión 1.1 (12–14 semanas):**

   * Expansión de clases (placa, cálculo, aftas, úlceras — según datos).
   * Mapas de calor (Grad‑CAM) y explicación de la predicción.
   * Notificaciones (email/WhatsApp) y recordatorios de higiene/citas.
3. **Versión 1.2 (16+ semanas):**

   * **CRM** para clínicas: embudo de pacientes, campañas, NPS.
   * **ERP liviano**: agenda, stock básico, órdenes de servicio, facturación ligera.

---

## 3) Público objetivo y propuesta de valor

* **Personas** que desean control preventivo y registro de su salud dental.
* **Clínicas/odontólogos** que buscan pre‑triaje, seguimiento y retención.

**Valor:** detección temprana + seguimiento visual, mejora de adherencia, reducción de consultas innecesarias y mayor educación del paciente.

---

## 4) Alcance funcional (MVP)

* **Auth & perfiles:** registro (email/Google), login, recuperación de contraseña, 2FA opcional.
* **Captura/subida:** cámara web/móvil, drag‑and‑drop, validación básica (iluminación, enfoque).
* **Inferencia IA:** API /inference que retorna probabilidades por clase + etiqueta final.
* **Historial:** galería por usuario, línea de tiempo, comparativas por fecha/clase.
* **Dashboard:** métricas personales (último resultado, tendencia, hábitos recordados).
* **Reportes:** PDF con resumen de hallazgos y consejos (no diagnóstico).
* **Privacidad:** consentimiento, gestión de datos y borrado bajo solicitud.

**Versión clínica (opcional):**

* Panel de pacientes (consentimiento explícito), vistas por caso, envío de recordatorios.

---

## 5) IA: diseño del modelo y MLOps

### 5.1. Problema

Clasificación **multi‑etiqua** (caries, gingivitis, sin hallazgos; extensible). Opcional: detección/segmentación para localizar lesiones.

### 5.2. Datos

* Fuentes: datasets públicos + acuerdos con clínicas + captura controlada beta.
* Anotación: 2+ odontólogos por imagen, consenso, etiquetas por diente/segmento.
* Balanceo: *class weighting*, oversampling, *focal loss* si hay desbalance.

### 5.3. Arquitectura de modelo

* **Backbone eficiente** (MobileNetV3/EfficientNet‑B0) → **TFLite** para edge o server.
* Aumento de datos (brightness, rotation, cutout) + normalización fotométrica.
* Entrenamiento: *transfer learning* + *fine‑tuning* gradual.
* Métricas: **AUROC macro**, **sensibilidad/especificidad por clase**, **F1**.
* Explicabilidad: **Grad‑CAM** / **Score‑CAM**.

### 5.4. Servir el modelo

* **Opción A (server):** FastAPI + ONNX Runtime/TensorRT; autoscaling.
* **Opción B (edge):** TFLite en navegador vía WebAssembly/WebGPU (piloto).

### 5.5. MLOps

* Versionado de datos/modelos: **DVC** o **MLflow**.
* Experimentos: **Weights & Biases** o MLflow Tracking.
* CI/CD de modelos (promoción por métricas y tests de sesgo/robustez).
* Monitorización en producción: *drift*, tasa de FN, latencia, *feedback loop*.

---

## 6) Arquitectura técnica

**Frontend (Web):** Next.js (React), TypeScript, Tailwind, Upload de cámara (MediaDevices), PWA.

**Backend (API):** FastAPI (Python) para inferencia y orquestación; o NestJS (Node) para capa de negocio. JWT + OAuth 2.0, RBAC (roles: usuario, clínico, admin).

**Base de datos:** PostgreSQL (usuarios, metadatos), **S3‑compatible** (MinIO/AWS S3) para imágenes; Redis para colas/cache.

**Infraestructura:** Docker + Docker Compose; despliegue en **Railway/Render/AWS/GCP**. CDN para imágenes. Autoscaling (K8s opcional v2).

**Observabilidad:** OpenTelemetry, Prometheus, Grafana, Sentry.

**Seguridad:** HTTPS, HSTS, CSP, sanitización, *rate limiting*, cifrado en reposo (KMS), rotación de claves, backups automatizados.

**Cumplimiento:** Consentimiento explícito, *privacy by design*, *data minimization*, términos/privacidad, *right to delete*; orientación HIPAA/GDPR‑like (no consejo médico, solo apoyo).

---

## 7) Diseño de datos (ERD textual)

* **users**(id, name, email, password_hash, auth_provider, role, created_at)
* **photos**(id, user_id, path, taken_at, device, quality_score, created_at)
* **inferences**(id, photo_id, model_version, probs_json, label_final, explain_uri, created_at)
* **habits**(id, user_id, brushing_per_day, floss_per_week, last_checkup_at)
* **alerts**(id, user_id, type, schedule_at, status)
* **clinics**(id, name, contact, owner_user_id)
* **patients_clinic**(clinic_id, user_id, consent_signed_at, tags)
* **appointments**(id, clinic_id, user_id, starts_at, status, notes)
* **inventory**(id, clinic_id, item, qty, reorder_point)  *(ERP básico)*
* **orders**(id, clinic_id, patient_id, amount, status)  *(ERP básico)*

---

## 8) API (borrador de endpoints)

**Auth**

* POST /auth/register, POST /auth/login, POST /auth/refresh, POST /auth/forgot

**Usuarios & fotos**

* GET /me
* POST /photos (multipart, admite cámara)
* GET /photos?user_id=me, GET /photos/{id}

**Inferencia**

* POST /inference/{photo_id}
* GET /inference/{photo_id}

**Reportes**

* GET /reports/{user_id}/latest (PDF)

**Clínicas (opcional)**

* GET/POST /clinics, GET/POST /appointments, GET/POST /patients

---

## 9) UX/UI (MVP)

* **Onboarding** con consentimiento y guía de foto (iluminación, ángulo, higiene).
* **Captura guiada** con marco de referencia y *quality score* instantáneo.
* **Pantalla de resultado** clara: semáforo, etiquetas, mapa de calor.
* **Historial** con línea de tiempo y comparador (antes/después).
* **Accesibilidad:** WCAG AA, textos educativos breves, lenguaje claro.

---

## 10) Integración CRM y ERP (ideas concretas)

### 10.1. CRM (relación con pacientes)

* **360 del paciente:** último resultado, riesgos, adherencia a hábitos.
* **Campañas personalizadas:** emails/WhatsApp con educación preventiva.
* **Embudo:** captación → activación → retención → reactivación.
* **NPS** y encuestas post‑reporte; scoring de propensión a cita.

### 10.2. ERP (operación de clínica)

* **Agenda inteligente:** predice ausentismo, sugiere slots.
* **Inventario básico:** insumos de profilaxis, resinas; alertas de reposición.
* **Facturación ligera:** órdenes, estados de pago, reportes mensuales.

*Nota:* CRM/ERP son módulos **opcionales** e independientes, activables por clínicas; el usuario final mantiene control sobre su información y consentimientos.

---

## 11) Métricas de éxito (KPIs)

* **IA:** AUROC ≥ 0.90 (caries), sensibilidad ≥ 0.85; falsos negativos < 10%.
* **Producto:** tasa de activación (captura exitosa) > 70%; retención 30d > 25%.
* **Tiempo de inferencia:** p95 < 800 ms (server) o < 200 ms (edge local).

---

## 12) Roadmap y estimación

**Semana 1–2:** Diseño UX, arquitectura, base de datos, setup CI/CD.

**Semana 3–4:** Auth, subida/captura, almacenamiento S3, endpoints CRUD.

**Semana 5–6:** Primer modelo IA (transfer learning), servicio de inferencia, Grad‑CAM.

**Semana 7–8:** Dashboard, historial, reportes PDF, pruebas, endurecimiento seguridad.

**Semana 9–10:** Beta cerrada, telemetría, mejora de modelo, documentación.

**Opcional v1.1–1.2:** Mapas de calor avanzados, campañas CRM, agenda ERP.

---

## 13) Stack recomendado

* **Frontend:** Next.js, TypeScript, Tailwind, Zustand/Redux.
* **Backend:** FastAPI (Python) + Uvicorn/Gunicorn; o NestJS si se prioriza TS end‑to‑end.
* **IA:** PyTorch/TensorFlow, Torch‑TensorRT/ONNX Runtime, TFLite (edge), OpenCV.
* **Datos:** PostgreSQL, MinIO/AWS S3, Redis, DVC/MLflow.
* **Infra:** Docker, Nginx, Terraform (si cloud), Grafana/Prometheus, Sentry.
* **Notificaciones:** SendGrid/Mailgun, Twilio/WhatsApp.

---

## 14) Seguridad, ética y cumplimiento

* **No es diagnóstico médico.** Se muestra descargo y se recomienda consulta profesional.
* **Consentimiento informado** para uso de imágenes y para compartir con clínicas.
* **Pseudonimización** de imágenes; cifrado AES‑256 en reposo y TLS en tránsito.
* **Controles de acceso** estrictos; auditoría de accesos a imágenes.
* **Derechos ARCO** (acceso/rectificación/cancelación/oposición) y borrado.
* **Sesgo y equidad:** evaluación por tono de piel, edad, tipo de cámara; *thresholds* adaptativos.

---

## 15) Testing y calidad

* **Unit tests** (80% cobertura), **integration/e2e** (Playwright/Cypress).
* **Conjuntos de validación estratificados** por dispositivo y condiciones de luz.
* **Ensayos A/B** para UX de captura y mensajes educativos.

---

## 16) Entregables para CV/portfolio

* **Repositorio Git público** (sin datos sensibles) con README profesional.
* **Demo en vivo** (Railway/Render) + **video demo** (2–3 min) con casos reales.
* **Documento técnico** (este) y **arquitectura** (diagramas), **hoja de ruta** y KPIs.
* **Cuaderno de experimentos** (W&B/MLflow) con comparativas de modelos.

---

## 17) Próximos pasos inmediatos

1. Definir clases objetivo del MVP (caries, gingivitis, “sin hallazgos”).
2. Cerrar stack (FastAPI + Next.js + PostgreSQL + S3 + PyTorch/TFLite).
3. Preparar guía de captura y dataset semilla; establecer protocolo de anotación.
4. Configurar repos, CI/CD y plantillas de infraestructura.
5. Calendarizar sprints (8–10 semanas) y abrir un beta con 10–20 usuarios.

---

### Anexo A: Diagrama lógico (alto nivel)

**Cliente (web/PWA)** → **API Gateway (Nginx)** → **Backend (FastAPI)** → **Servicio de IA (ONNX/TensorRT)** → **PostgreSQL** (metadatos) y **S3/MinIO** (imágenes) → **MLflow/DVC** (versionado) → **Grafana/Prometheus** (métricas) → **Sentry** (errores).

### Anexo B: Política de privacidad (borrador)

* Finalidad: monitoreo de salud bucal con IA y mejora del servicio.
* Base legal: consentimiento explícito del usuario.
* Conservación: hasta que el usuario solicite borrado o cierre de cuenta.
* Compartición: jamás sin consentimiento (salvo obligación legal).
