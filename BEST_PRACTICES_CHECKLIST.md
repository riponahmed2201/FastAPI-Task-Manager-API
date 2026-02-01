# FastAPI Best Practices - Quick Reference Checklist

A quick checklist for implementing and maintaining best practices in your FastAPI applications.

---

## 🔒 Security Checklist

### Secrets & Configuration
- [ ] All secrets stored in `.env` file
- [ ] `.env` file added to `.gitignore`
- [ ] `.env.example` created without secrets
- [ ] Use `pydantic-settings` for configuration
- [ ] Environment variables validated at startup
- [ ] Different configs for dev/test/production

### Authentication & Authorization
- [ ] Passwords hashed with bcrypt (minimum 12 rounds)
- [ ] JWT tokens with expiration times
- [ ] Refresh token mechanism implemented
- [ ] OAuth2PasswordBearer used for security scheme
- [ ] User authentication dependency created
- [ ] Rate limiting implemented on auth endpoints
- [ ] Account lockout after failed attempts (optional)

### Input Validation
- [ ] All inputs validated with Pydantic
- [ ] Field length limits enforced
- [ ] Email validation used
- [ ] SQL injection prevention (SQLAlchemy ORM)
- [ ] XSS prevention through output escaping
- [ ] CSRF protection implemented (if applicable)

### API Security
- [ ] CORS configured with specific origins (not `*`)
- [ ] HTTPS enforced in production
- [ ] Security headers added (HSTS, X-Content-Type-Options, etc.)
- [ ] API versioning implemented
- [ ] Rate limiting configured
- [ ] Request size limits set

### Database Security
- [ ] Database credentials not hardcoded
- [ ] Connection pooling configured
- [ ] Read-only database users where possible
- [ ] Regular backups scheduled
- [ ] Database encryption enabled (production)

---

## ⚡ Performance Checklist

### Database Optimization
- [ ] Database indexes created for frequently queried columns
- [ ] N+1 query problems identified and fixed
- [ ] Eager loading (joinedload) used where appropriate
- [ ] Query results limited with pagination
- [ ] Connection pooling configured
- [ ] Slow queries monitored and optimized

### API Response
- [ ] Response compression (gzip) enabled
- [ ] Unnecessary data excluded from responses
- [ ] Pagination implemented for list endpoints
- [ ] Caching strategy implemented
- [ ] Response models optimized (exclude unnecessary fields)

### Async/Concurrency
- [ ] Async operations used for I/O
- [ ] Long-running tasks offloaded to background jobs
- [ ] WebSocket connections for real-time updates (if applicable)
- [ ] Connection pooling for database

### Monitoring
- [ ] Response times monitored
- [ ] Error rates tracked
- [ ] Database performance monitored
- [ ] Uptime monitoring configured
- [ ] Resource usage (CPU, memory) monitored

---

## 🧪 Testing Checklist

### Unit Tests
- [ ] Test coverage > 80%
- [ ] All functions have tests
- [ ] Edge cases covered
- [ ] Mocking external dependencies
- [ ] Database tests use test database
- [ ] Tests run in isolation

### Integration Tests
- [ ] API endpoints tested end-to-end
- [ ] Database interactions tested
- [ ] Authentication flows tested
- [ ] Error scenarios tested

### Security Tests
- [ ] SQL injection tested
- [ ] XSS vulnerability tested
- [ ] CSRF protection tested
- [ ] Authentication bypass tested
- [ ] Authorization bypass tested
- [ ] Rate limiting tested

### Test Infrastructure
- [ ] pytest configured
- [ ] Test fixtures created
- [ ] CI/CD pipeline includes tests
- [ ] Code coverage measured
- [ ] Test data/fixtures managed

---

## 📝 Code Quality Checklist

### Code Organization
- [ ] Modular structure (models, schemas, crud, routers)
- [ ] Separation of concerns maintained
- [ ] DRY principle followed
- [ ] SOLID principles applied
- [ ] Functions/methods have single responsibility

### Code Style
- [ ] Type hints throughout code
- [ ] Consistent naming conventions (snake_case, PascalCase)
- [ ] PEP 8 followed (use black formatter)
- [ ] Docstrings for all functions
- [ ] Comments explain "why", not "what"

### Validation
- [ ] All inputs validated
- [ ] Error messages clear and helpful
- [ ] Custom exceptions created for domain logic
- [ ] Logging added for debugging

### Documentation
- [ ] README.md comprehensive
- [ ] API endpoints documented
- [ ] Code comments where needed
- [ ] Type hints as inline documentation
- [ ] Docstrings follow conventions
- [ ] Examples provided for common tasks

---

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Security audit completed
- [ ] Performance tested under load
- [ ] Database migrations tested
- [ ] Environment variables set

### Deployment Infrastructure
- [ ] Docker image created
- [ ] Docker Compose configured
- [ ] Nginx reverse proxy configured
- [ ] SSL/TLS certificates obtained
- [ ] Database backups configured
- [ ] Monitoring/logging setup

### Application Setup
- [ ] Environment-specific configs created
- [ ] Database migrations applied
- [ ] Initial data seeded (if needed)
- [ ] Health checks working
- [ ] Logging configured
- [ ] Error tracking (Sentry) configured

### Post-Deployment
- [ ] Health check endpoint responds
- [ ] Logs being collected
- [ ] Monitoring alerts configured
- [ ] Performance baseline established
- [ ] Backup verified
- [ ] Rollback plan in place

---

## 🔄 Development Workflow Checklist

### Version Control
- [ ] Git configured properly
- [ ] `.gitignore` configured
- [ ] Feature branches used
- [ ] Meaningful commit messages
- [ ] Pull requests reviewed before merge
- [ ] Commit history is clean

### Code Review
- [ ] Code follows project style
- [ ] Tests pass
- [ ] No security issues
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] No hardcoded values

### CI/CD
- [ ] GitHub Actions configured
- [ ] Linting checks pass (flake8, black)
- [ ] Type checking passes (mypy)
- [ ] Tests pass
- [ ] Coverage maintained
- [ ] Automated deployment on main

### Dependencies
- [ ] requirements.txt maintained
- [ ] requirements-dev.txt for dev dependencies
- [ ] Dependency versions pinned
- [ ] Security updates monitored
- [ ] Deprecated packages replaced
- [ ] Minimal dependencies (no bloat)

---

## 📊 Monitoring & Maintenance Checklist

### Logging
- [ ] Structured logging implemented
- [ ] Appropriate log levels used
- [ ] Log rotation configured
- [ ] Log aggregation setup
- [ ] Sensitive data not logged

### Alerts
- [ ] Error rate alerts
- [ ] High response time alerts
- [ ] Database connection alerts
- [ ] Disk space alerts
- [ ] Memory usage alerts
- [ ] CPU usage alerts

### Regular Maintenance
- [ ] Dependency updates checked monthly
- [ ] Security patches applied immediately
- [ ] Database maintenance scheduled
- [ ] Log cleanup scheduled
- [ ] Performance review quarterly
- [ ] Architecture review annually

### Backup & Disaster Recovery
- [ ] Daily backups scheduled
- [ ] Backup verification automated
- [ ] Restore procedure documented
- [ ] Disaster recovery plan written
- [ ] DR plan tested quarterly
- [ ] Recovery time objective (RTO) defined

---

## 🎯 API Design Checklist

### RESTful Design
- [ ] HTTP verbs used correctly (GET, POST, PUT, PATCH, DELETE)
- [ ] Status codes correct (200, 201, 204, 400, 401, 403, 404, 500)
- [ ] Resource-oriented URLs
- [ ] Consistent URL structure
- [ ] No verbs in URLs
- [ ] Proper HTTP semantics

### Response Format
- [ ] Consistent JSON structure
- [ ] Error responses standardized
- [ ] Response models defined
- [ ] Pagination schema consistent
- [ ] Filtering/sorting parameters clear
- [ ] Timestamps in ISO 8601 format

### Documentation
- [ ] OpenAPI/Swagger specs accurate
- [ ] Interactive docs working
- [ ] API examples provided
- [ ] Endpoint descriptions clear
- [ ] Parameter descriptions clear
- [ ] Error codes documented

### Versioning
- [ ] API versioning strategy defined
- [ ] Version in URL path (`/api/v1/`)
- [ ] Backward compatibility maintained
- [ ] Deprecation warnings provided
- [ ] Migration guide for version changes
- [ ] Support timeline for old versions

---

## 📋 Configuration Management Checklist

### Environment Variables
- [ ] All config in environment variables
- [ ] No hardcoded values
- [ ] `.env` file for local development
- [ ] `.env.example` provided
- [ ] Different configs per environment
- [ ] Environment validation at startup

### Settings Management
- [ ] BaseSettings used from pydantic
- [ ] Settings cached with @lru_cache
- [ ] Hierarchical configs (base, dev, test, prod)
- [ ] Type hints on all settings
- [ ] Default values reasonable
- [ ] Required values enforced

### Secrets Management
- [ ] Secrets in `.env` or environment
- [ ] Secrets never committed to git
- [ ] Secrets rotated regularly
- [ ] Secrets encrypted in transit
- [ ] Access to secrets audited
- [ ] Secrets manager used (production)

---

## 🧬 Database Checklist

### Schema Design
- [ ] Normalized schema (at least 3NF)
- [ ] Primary keys defined
- [ ] Foreign keys with cascade
- [ ] Indexes on frequently queried columns
- [ ] Unique constraints where needed
- [ ] Check constraints for data integrity

### Migrations
- [ ] Alembic configured for migrations
- [ ] All schema changes in migrations
- [ ] Migrations tested
- [ ] Rollback procedure tested
- [ ] Migration history maintained
- [ ] Downtime minimized for production migrations

### Data Management
- [ ] Data validation at application level
- [ ] Soft deletes (if applicable)
- [ ] Audit logs for important changes
- [ ] Data retention policy defined
- [ ] GDPR compliance considered
- [ ] Regular data cleanup scheduled

---

## Summary Usage

### For New Features
1. Review Security Checklist
2. Review Code Quality Checklist
3. Review Testing Checklist
4. Review API Design Checklist

### Before Deployment
1. Complete Testing Checklist
2. Complete Pre-Deployment Checklist
3. Complete Deployment Infrastructure Checklist
4. Review Monitoring & Maintenance Checklist

### For Code Reviews
1. Review Code Quality Checklist
2. Review Security Checklist
3. Review API Design Checklist
4. Check tests are added

### For Operations
1. Review Monitoring & Maintenance Checklist
2. Review Deployment Checklist
3. Review Backup & Disaster Recovery items
4. Review Configuration Management items

---

**Last Updated**: February 1, 2026  
**Version**: 1.0  
**For**: Task Manager API  

Print this checklist and use it as a reference during development!
