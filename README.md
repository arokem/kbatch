# kbatch

Submit batch jobs to JupyterHub.

*also*

An asynchronous / batch complement to what JupyterHub already provides.

## Desiderata

- **Simplicity of implementation**: https://words.yuvi.in/post/kbatch/ by Yuvi Panda captures this well.
- **Simplicity of use**: Ideally users don't need to adapt their script / notebook / unit of work to the job system.
- **Integration with JupyterHub**: Runs as a JupyterHub services, uses JupyterHub for auth, etc.
- **Runs on Kubernetes**: mainly for the simplicity of implementation, and also that's my primary use-case.
- **Users do not have access to the Kubernetes API**: partly because if users need to know about Kubernetes then we've failed, and partly for security.

Together, these rule some great tools like [Argo workflows](https://argoproj.github.io/workflows), [Ploomber](https://github.com/ploomber/ploomber), [Elyra](https://github.com/elyra-ai/elyra). So we write our own (hopefully simple) implementation.

## Architecture

Because end-users don't have access to the Kubernetes API, we have a client/server model. Users make API requests to the server to submit / list / show jobs.

The server is split into two parts: a frontend that handles requests, and a backend that submits them to Kubernetes.

## Usage (hypothetical)

Authenticate with the server

```
$ kbatch login https://url-to-kbatch-server
```

This will create configuration file that specifies the default URL and credentials to use for all `kbatch` operations.

Submit a job

```
$ kbatch submit myscript.py --image=...
...
```

List jobs

```
$ kbatch jobs list
...
```

Show the detail on a given job

```
$ kbatch jobs show --job-id=...
```