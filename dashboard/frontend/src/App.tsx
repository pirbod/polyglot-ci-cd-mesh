import { useEffect, useMemo, useState } from 'react';
import {
  Activity,
  Box,
  Cloud,
  Download,
  GitBranch,
  type LucideIcon,
  Play,
  RotateCcw,
  ShieldCheck,
  ShieldAlert,
  Sparkles,
} from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8080';

type Pipeline = {
  id: string;
  service: string;
  runtime: string;
  build: string;
  tests: string;
  scan: string;
  image: string;
  sbom: string;
  attestation: string;
  deploy_readiness: string;
  risk_score: number;
  last_run: string;
};

type PipelineRun = {
  id: string;
  service: string;
  status: string;
  duration_seconds: number;
  created_at: string;
};

type CloudTarget = {
  id: string;
  name: string;
  cluster: string;
  region: string;
  terraform_plan: string;
  registry: string;
  argocd_sync: string;
  health: string;
  environment: string;
};

type Finding = {
  code: string;
  severity: string;
  message: string;
  remediation: string;
  location: string;
};

type ApiGate = {
  selected: string;
  last_result: {
    status: string;
    risk_score: number;
    findings: Finding[];
    remediation: string[];
  };
};

type GitOpsApp = {
  id: string;
  service: string;
  cluster: string;
  sync: string;
  health: string;
  revision: string;
  wave: number;
};

type Evidence = {
  name: string;
  path: string;
  type: string;
};

type MeshState = {
  overview: {
    mesh_health_score: number;
    build_success_rate: number;
    deployment_readiness: number;
    security_gate_status: string;
    supply_chain_risk_score: number;
  };
  pipelines: Pipeline[];
  pipeline_runs: PipelineRun[];
  clouds: CloudTarget[];
  api_gate: ApiGate;
  supply_chain: Record<string, string>;
  gitops: GitOpsApp[];
  evidence: Evidence[];
};

const nav = [
  { id: 'overview', label: 'Overview', icon: Activity },
  { id: 'pipelines', label: 'Pipelines', icon: Play },
  { id: 'cloud', label: 'Cloud', icon: Cloud },
  { id: 'api', label: 'API Gate', icon: ShieldCheck },
  { id: 'supply', label: 'Supply Chain', icon: Box },
  { id: 'gitops', label: 'GitOps', icon: GitBranch },
  { id: 'evidence', label: 'Evidence', icon: Download },
];

function Badge({ value }: { value: string }) {
  const tone = value.toLowerCase();
  const classes = tone.includes('fail') || tone.includes('blocked') || tone.includes('outofsync')
    ? 'bg-red-50 text-danger border-red-200'
    : tone.includes('warn') || tone.includes('progress') || tone.includes('simulated')
      ? 'bg-amber-50 text-warning border-amber-200'
      : 'bg-emerald-50 text-success border-emerald-200';
  return <span className={`inline-flex rounded-full border px-2.5 py-1 text-xs font-semibold ${classes}`}>{value}</span>;
}

function Metric({ label, value, suffix = '' }: { label: string; value: number | string; suffix?: string }) {
  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-sm">
      <p className="text-sm font-medium text-slate-500">{label}</p>
      <p className="mt-3 text-4xl font-bold text-ink">{value}{suffix}</p>
    </section>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-sm">
      <h2 className="text-lg font-bold text-ink">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function ActionButton({ children, onClick, icon: Icon }: { children: React.ReactNode; onClick: () => void; icon: LucideIcon }) {
  return (
    <button
      onClick={onClick}
      className="inline-flex items-center gap-2 rounded-md bg-action px-3 py-2 text-sm font-semibold text-white transition hover:bg-blue-700"
    >
      <Icon size={16} aria-hidden="true" />
      {children}
    </button>
  );
}

export function App() {
  const [page, setPage] = useState('overview');
  const [state, setState] = useState<MeshState | null>(null);
  const [apiResult, setApiResult] = useState<ApiGate['last_result'] | null>(null);

  async function refresh() {
    const response = await fetch(`${API_URL}/api/state`);
    setState(await response.json());
  }

  useEffect(() => {
    refresh();
  }, []);

  const content = useMemo(() => {
    if (!state) return <Panel title="Loading">Preparing local evidence.</Panel>;
    if (page === 'pipelines') return <Pipelines state={state} refresh={refresh} />;
    if (page === 'cloud') return <CloudDelivery state={state} refresh={refresh} />;
    if (page === 'api') return <ApiGateView state={state} apiResult={apiResult} setApiResult={setApiResult} />;
    if (page === 'supply') return <SupplyChain state={state} />;
    if (page === 'gitops') return <GitOps state={state} refresh={refresh} />;
    if (page === 'evidence') return <EvidenceCenter state={state} />;
    return <Overview state={state} />;
  }, [page, state, apiResult]);

  return (
    <main className="min-h-screen bg-cloud text-ink">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-5 px-5 py-5 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-slate-500">Local-first enterprise PoC</p>
            <h1 className="mt-1 text-3xl font-bold">Polyglot CI/CD Mesh</h1>
          </div>
          <nav className="flex flex-wrap gap-2">
            {nav.map((item) => {
              const Icon = item.icon;
              const active = item.id === page;
              return (
                <button
                  key={item.id}
                  onClick={() => setPage(item.id)}
                  className={`inline-flex items-center gap-2 rounded-md border px-3 py-2 text-sm font-semibold transition ${
                    active ? 'border-action bg-blue-50 text-action' : 'border-line bg-white text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <Icon size={16} aria-hidden="true" />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>
      </header>
      <div className="mx-auto max-w-7xl px-5 py-6">{content}</div>
    </main>
  );
}

function Overview({ state }: { state: MeshState }) {
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase text-slate-500">Executive Overview</p>
          <h2 className="mt-1 text-2xl font-bold">Mesh command center</h2>
        </div>
        <Badge value={state.overview.security_gate_status} />
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <Metric label="Mesh health" value={state.overview.mesh_health_score} />
        <Metric label="Build success" value={state.overview.build_success_rate} suffix="%" />
        <Metric label="Readiness" value={state.overview.deployment_readiness} suffix="%" />
        <Metric label="API gate" value={state.overview.security_gate_status} />
        <Metric label="Supply risk" value={state.overview.supply_chain_risk_score} />
      </div>
      <Panel title="Cloud targets">
        <div className="grid gap-3 md:grid-cols-3">
          {state.clouds.map((cloud) => (
            <div key={cloud.id} className="rounded-lg border border-line p-4">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-bold">{cloud.name}</h3>
                  <p className="mt-1 text-sm text-slate-500">{cloud.cluster} · {cloud.region}</p>
                </div>
                <Badge value={cloud.health} />
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                <Badge value={cloud.terraform_plan} />
                <Badge value={cloud.argocd_sync} />
              </div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}

function Pipelines({ state, refresh }: { state: MeshState; refresh: () => Promise<void> }) {
  async function run(service_id: string) {
    await fetch(`${API_URL}/api/pipelines/run`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ service_id }),
    });
    await refresh();
  }
  return (
    <div className="grid gap-5 xl:grid-cols-[1fr_360px]">
      <Panel title="Runtime delivery cards">
        <div className="grid gap-4 md:grid-cols-2">
          {state.pipelines.map((pipeline) => (
            <article key={pipeline.id} className="rounded-lg border border-line p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="font-bold">{pipeline.service}</h3>
                  <p className="mt-1 text-sm text-slate-500">{pipeline.runtime} · risk {pipeline.risk_score}</p>
                </div>
                <ActionButton icon={Play} onClick={() => run(pipeline.id)}>Run</ActionButton>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {[pipeline.build, pipeline.tests, pipeline.scan, pipeline.image, pipeline.sbom, pipeline.attestation, pipeline.deploy_readiness].map((item) => (
                  <Badge key={item} value={item} />
                ))}
              </div>
            </article>
          ))}
        </div>
      </Panel>
      <Panel title="Run history">
        <div className="space-y-3">
          {state.pipeline_runs.map((run) => (
            <div key={run.id} className="rounded-lg border border-line p-3">
              <div className="flex items-center justify-between">
                <strong>{run.id}</strong>
                <Badge value={run.status} />
              </div>
              <p className="mt-1 text-sm text-slate-500">{run.service} · {run.duration_seconds}s</p>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}

function CloudDelivery({ state, refresh }: { state: MeshState; refresh: () => Promise<void> }) {
  async function promote() {
    await fetch(`${API_URL}/api/clouds/promote`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ environment: 'prod' }),
    });
    await refresh();
  }
  return (
    <Panel title="Multi-cloud delivery">
      <div className="mb-4 flex justify-end">
        <ActionButton icon={Sparkles} onClick={promote}>Promote to prod</ActionButton>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {state.clouds.map((cloud) => (
          <div key={cloud.id} className="rounded-lg border border-line p-4">
            <h3 className="font-bold">{cloud.name}</h3>
            <p className="mt-1 text-sm text-slate-500">{cloud.cluster}</p>
            <dl className="mt-4 space-y-3 text-sm">
              <Row label="Environment" value={cloud.environment} />
              <Row label="Terraform" value={cloud.terraform_plan} />
              <Row label="Registry" value={cloud.registry} />
              <Row label="ArgoCD" value={cloud.argocd_sync} />
            </dl>
          </div>
        ))}
      </div>
    </Panel>
  );
}

function ApiGateView({ state, apiResult, setApiResult }: { state: MeshState; apiResult: ApiGate['last_result'] | null; setApiResult: (value: ApiGate['last_result']) => void }) {
  async function select(filename: string) {
    const response = await fetch(`${API_URL}/api/openapi/select`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ filename }),
    });
    setApiResult(await response.json());
  }
  const result = apiResult ?? state.api_gate.last_result;
  return (
    <div className="grid gap-5 xl:grid-cols-[320px_1fr]">
      <Panel title="Spec samples">
        <div className="space-y-3">
          <ActionButton icon={ShieldCheck} onClick={() => select('compliant-api.yaml')}>Compliant</ActionButton>
          <ActionButton icon={ShieldAlert} onClick={() => select('non-compliant-api.yaml')}>Non-compliant</ActionButton>
        </div>
      </Panel>
      <Panel title="Policy result">
        <div className="flex flex-wrap items-center gap-3">
          <Badge value={result.status} />
          <span className="text-sm font-semibold text-slate-600">Risk score {result.risk_score}</span>
        </div>
        <div className="mt-4 space-y-3">
          {result.findings.length === 0 ? (
            <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-success">All API policy checks passed.</div>
          ) : (
            result.findings.map((finding) => (
              <div key={`${finding.code}-${finding.location}`} className="rounded-lg border border-red-200 bg-red-50 p-4">
                <div className="flex items-center justify-between gap-3">
                  <strong>{finding.message}</strong>
                  <Badge value={finding.severity} />
                </div>
                <p className="mt-2 text-sm text-slate-700">{finding.remediation}</p>
              </div>
            ))
          )}
        </div>
      </Panel>
    </div>
  );
}

function SupplyChain({ state }: { state: MeshState }) {
  return (
    <Panel title="Supply-chain security">
      <div className="grid gap-4 md:grid-cols-2">
        {Object.entries(state.supply_chain).map(([key, value]) => (
          <div key={key} className="rounded-lg border border-line p-4">
            <p className="text-sm font-semibold uppercase text-slate-500">{key.replaceAll('_', ' ')}</p>
            <p className="mt-2 font-medium">{value}</p>
          </div>
        ))}
      </div>
    </Panel>
  );
}

function GitOps({ state, refresh }: { state: MeshState; refresh: () => Promise<void> }) {
  async function rollback(app_id: string) {
    await fetch(`${API_URL}/api/gitops/rollback`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ app_id }),
    });
    await refresh();
  }
  return (
    <Panel title="Apps-of-apps topology">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="text-slate-500">
            <tr>
              <th className="py-2">Service</th>
              <th>Cluster</th>
              <th>Sync</th>
              <th>Health</th>
              <th>Revision</th>
              <th>Wave</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {state.gitops.map((app) => (
              <tr key={app.id} className="border-t border-line">
                <td className="py-3 font-semibold">{app.service}</td>
                <td>{app.cluster}</td>
                <td><Badge value={app.sync} /></td>
                <td><Badge value={app.health} /></td>
                <td className="font-mono text-xs">{app.revision}</td>
                <td>{app.wave}</td>
                <td className="text-right">
                  <button onClick={() => rollback(app.id)} className="inline-flex items-center gap-2 rounded-md border border-line px-3 py-2 font-semibold text-slate-700 hover:bg-slate-50">
                    <RotateCcw size={15} aria-hidden="true" />
                    Rollback
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Panel>
  );
}

function EvidenceCenter({ state }: { state: MeshState }) {
  return (
    <Panel title="Evidence center">
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {state.evidence.map((item) => (
          <a key={item.name} href={`${API_URL}/api/evidence/${item.name}`} className="rounded-lg border border-line p-4 transition hover:border-action hover:bg-blue-50">
            <div className="flex items-center justify-between gap-3">
              <strong>{item.name}</strong>
              <Download size={18} aria-hidden="true" />
            </div>
            <p className="mt-2 text-sm text-slate-500">{item.path}</p>
          </a>
        ))}
      </div>
    </Panel>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4">
      <dt className="text-slate-500">{label}</dt>
      <dd><Badge value={value} /></dd>
    </div>
  );
}
