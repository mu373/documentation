import React, {useMemo, useRef, useState} from 'react';
import katex from 'katex';
import styles from './styles.module.css';

type Mode = 'edge' | 'degree' | 'free';

const accentBlue = 'var(--ifm-color-primary)';
const coral = '#D85A30';
const masks = [0, 1, 2, 4, 3, 5, 6, 7];
const barCenters = [77, 129, 181, 233, 319, 371, 423, 509];
const barWidth = 42;
const edgeCounts = masks.map((mask) => (mask & 1) + ((mask >> 1) & 1) + ((mask >> 2) & 1));

function clamp(x: number, min: number, max: number) {
  return Math.max(min, Math.min(max, x));
}

function edgeProbsToP(edgeProbs: number[]) {
  return masks.map((mask) =>
    (mask & 1 ? edgeProbs[0] : 1 - edgeProbs[0]) *
    (mask & 2 ? edgeProbs[1] : 1 - edgeProbs[1]) *
    (mask & 4 ? edgeProbs[2] : 1 - edgeProbs[2]),
  );
}

function entropyBits(probabilities: number[]) {
  return probabilities.reduce((sum, probability) => {
    if (probability <= 1e-12) return sum;
    return sum - probability * Math.log2(probability);
  }, 0);
}

function meanEdges(probabilities: number[]) {
  return probabilities.reduce((sum, probability, index) => sum + probability * edgeCounts[index], 0);
}

function maxEntropyBits(mean: number) {
  const p = mean / 3;
  if (p <= 1e-9 || p >= 1 - 1e-9) return 0;
  return 3 * (-p * Math.log2(p) - (1 - p) * Math.log2(1 - p));
}

function formatPct(probability: number) {
  const value = probability * 100;
  return `${value < 9.95 ? value.toFixed(1) : value.toFixed(0)}%`;
}

function InlineMath({tex}: {tex: string}) {
  const html = useMemo(() => katex.renderToString(tex, {throwOnError: false}), [tex]);

  return <span className={styles.inlineMath} dangerouslySetInnerHTML={{__html: html}} />;
}

function MiniGraph({mask, x, y, width, height}: {mask: number; x: number; y: number; width: number; height: number}) {
  const a: [number, number] = [32, 12];
  const b: [number, number] = [14, 48];
  const c: [number, number] = [50, 48];
  const edges: Array<[number, [number, number], [number, number]]> = [
    [1, a, b],
    [2, a, c],
    [4, b, c],
  ];

  return (
    <svg x={x} y={y} width={width} height={height} viewBox="0 0 64 60">
      {edges
        .filter(([bit]) => mask & bit)
        .map(([bit, start, end]) => (
          <line
            key={bit}
            x1={start[0]}
            y1={start[1]}
            x2={end[0]}
            y2={end[1]}
            stroke="var(--mx-text-primary)"
            strokeWidth="2.6"
            strokeLinecap="round"
          />
        ))}
      {[a, b, c].map((point, index) => (
        <circle key={index} cx={point[0]} cy={point[1]} r="5" fill="var(--mx-text-primary)" />
      ))}
    </svg>
  );
}

function ProbabilityMassChart({
  probabilities,
  mode,
  onFreeProbabilityChange,
}: {
  probabilities: number[];
  mode: Mode;
  onFreeProbabilityChange: (index: number, probability: number) => void;
}) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const draggingIndex = useRef<number | null>(null);
  const yBase = 170;
  const height = 152;
  const yBar = (probability: number) => yBase - clamp(probability, 0, 1) * height;

  const probabilityFromPointer = (clientY: number) => {
    const rect = svgRef.current?.getBoundingClientRect();
    if (!rect) return 0;
    const svgY = ((clientY - rect.top) / rect.height) * 250;
    return clamp((yBase - svgY) / height, 0, 1);
  };

  const indexFromPointer = (clientX: number) => {
    const rect = svgRef.current?.getBoundingClientRect();
    if (!rect) return -1;
    const svgX = ((clientX - rect.left) / rect.width) * 600;
    let best = -1;
    let bestDistance = Number.POSITIVE_INFINITY;
    barCenters.forEach((center, index) => {
      const distance = Math.abs(svgX - center);
      if (distance < bestDistance) {
        best = index;
        bestDistance = distance;
      }
    });
    return bestDistance < barWidth * 0.9 ? best : -1;
  };

  const startDrag = (event: React.PointerEvent<SVGSVGElement>) => {
    if (mode !== 'free') return;
    const index = indexFromPointer(event.clientX);
    if (index < 0) return;
    draggingIndex.current = index;
    event.currentTarget.setPointerCapture(event.pointerId);
    onFreeProbabilityChange(index, probabilityFromPointer(event.clientY));
  };

  const updateDrag = (event: React.PointerEvent<SVGSVGElement>) => {
    if (draggingIndex.current == null) return;
    onFreeProbabilityChange(draggingIndex.current, probabilityFromPointer(event.clientY));
  };

  const stopDrag = () => {
    draggingIndex.current = null;
  };

  const groupCenters = [barCenters[0], (barCenters[1] + barCenters[3]) / 2, (barCenters[4] + barCenters[6]) / 2, barCenters[7]];

  return (
    <svg
      ref={svgRef}
      className={mode === 'free' ? styles.draggableChart : undefined}
      viewBox="0 0 600 250"
      width="100%"
      role="img"
      aria-label="Bar chart of the probability of each of the eight graphs, grouped by number of edges."
      onPointerDown={startDrag}
      onPointerMove={updateDrag}
      onPointerUp={stopDrag}
      onPointerCancel={stopDrag}
      onPointerLeave={stopDrag}
    >
      {[0, 0.25, 0.5, 0.75, 1].map((tick) => (
        <g key={tick}>
          <line x1="44" x2="588" y1={yBase - tick * height} y2={yBase - tick * height} stroke="var(--mx-border-tertiary)" />
          <text x="38" y={yBase - tick * height + 4} textAnchor="end" fill="var(--mx-text-tertiary)" fontSize="11">
            {tick}
          </text>
        </g>
      ))}
      {probabilities.map((probability, index) => (
        <g key={masks[index]}>
          <rect
            x={barCenters[index] - barWidth / 2}
            y={yBar(probability)}
            width={barWidth}
            height={yBase - yBar(probability)}
            rx="3"
            fill={accentBlue}
          />
          <text x={barCenters[index]} y={yBar(probability) - 5} textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="11">
            {formatPct(probability)}
          </text>
          <MiniGraph mask={masks[index]} x={barCenters[index] - 17} y={176} width={34} height={32} />
        </g>
      ))}
      {['0 Edges', '1 Edge', '2 Edges', '3 Edges'].map((label, index) => (
        <text key={label} x={groupCenters[index]} y="224" textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="12">
          {label}
        </text>
      ))}
      <text transform="translate(13,94) rotate(-90)" textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="12">
        Probability
      </text>
    </svg>
  );
}

function EdgeCountChart({probabilities, mean}: {probabilities: number[]; mean: number}) {
  const yBase = 108;
  const height = 90;
  const centers = [60, 128, 196, 264];
  const width = 40;
  const multiplicities = [1, 3, 3, 1];
  const edgeDistribution = probabilities.reduce(
    (distribution, probability, index) => {
      distribution[edgeCounts[index]] += probability;
      return distribution;
    },
    [0, 0, 0, 0],
  );
  const yBar = (probability: number) => yBase - clamp(probability, 0, 1) * height;
  const meanX = 60 + (mean / 3) * 204;

  return (
    <svg viewBox="0 0 300 158" role="img" aria-label="Bar chart of the edge count distribution.">
      {[0, 0.5, 1].map((tick) => (
        <g key={tick}>
          <line x1="40" x2="284" y1={yBase - tick * height} y2={yBase - tick * height} stroke="var(--mx-border-tertiary)" />
          <text x="34" y={yBase - tick * height + 4} textAnchor="end" fill="var(--mx-text-tertiary)" fontSize="11">
            {tick}
          </text>
        </g>
      ))}
      <line x1={meanX} x2={meanX} y1="14" y2={yBase} stroke={coral} strokeWidth="1.5" strokeDasharray="4 3" />
      {edgeDistribution.map((probability, edgeCount) => (
        <g key={edgeCount}>
          <rect
            x={centers[edgeCount] - width / 2}
            y={yBar(probability)}
            width={width}
            height={yBase - yBar(probability)}
            rx="3"
            fill={accentBlue}
          />
          <text x={centers[edgeCount]} y={yBar(probability) - 5} textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="11">
            {formatPct(probability)}
          </text>
          <text x={centers[edgeCount]} y="126" textAnchor="middle" fill="var(--mx-text-primary)" fontSize="13">
            {edgeCount}
          </text>
          <text x={centers[edgeCount]} y="142" textAnchor="middle" fill="var(--mx-text-tertiary)" fontSize="11">
            {multiplicities[edgeCount]} Graph{multiplicities[edgeCount] > 1 ? 's' : ''}
          </text>
        </g>
      ))}
    </svg>
  );
}

function EntropyChart({mean, entropy, entropyMax}: {mean: number; entropy: number; entropyMax: number}) {
  const xLeft = 46;
  const xRight = 586;
  const yTop = 20;
  const yBase = 267;
  const xPx = (edges: number) => xLeft + (edges / 3) * (xRight - xLeft);
  const yPx = (value: number) => yBase - (value / 3) * (yBase - yTop);
  const curve = Array.from({length: 151}, (_, index) => {
    const expectedEdges = (3 * index) / 150;
    return `${index === 0 ? 'M' : 'L'}${xPx(expectedEdges)} ${yPx(maxEntropyBits(expectedEdges))}`;
  }).join(' ');
  const x = xPx(mean);
  const gap = entropyMax - entropy;

  return (
    <svg viewBox="0 0 600 316" role="img" aria-label="Entropy in bits versus expected number of edges.">
      {[0, 1, 2, 3].map((tick) => (
        <g key={tick}>
          <line x1={xLeft} x2={xRight} y1={yPx(tick)} y2={yPx(tick)} stroke="var(--mx-border-tertiary)" />
          <text x={xLeft - 8} y={yPx(tick) + 6} textAnchor="end" fill="var(--mx-text-tertiary)" fontSize="16">
            {tick}
          </text>
        </g>
      ))}
      {[0, 1, 1.5, 2, 3].map((tick) => (
        <text key={tick} x={xPx(tick)} y={yBase + 21} textAnchor="middle" fill="var(--mx-text-tertiary)" fontSize="16">
          {tick}
        </text>
      ))}
      <path d={curve} fill="none" stroke={accentBlue} strokeWidth="2.5" />
      <line x1={xPx(1.5)} x2={xPx(1.5)} y1={yPx(3)} y2={yBase} stroke="var(--mx-border-tertiary)" strokeDasharray="3 3" />
      <text x={xPx(1.5) + 8} y={yBase - 8} fill="var(--mx-text-secondary)" fontSize="18" fontWeight="600">
        3 Bits = Uniform Over All 8
      </text>
      <text x="316" y="310" textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="17">
        Expected Edges &lt;L&gt;
      </text>
      <text transform="translate(17,144) rotate(-90)" textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="17">
        Entropy (Bits)
      </text>
      {gap < 0.012 ? (
        <>
          <line x1={x} x2={x} y1={yPx(entropy)} y2={yBase} stroke={accentBlue} strokeDasharray="3 3" />
          <circle cx={x} cy={yPx(entropy)} r="5.5" fill={accentBlue} />
        </>
      ) : (
        <>
          <circle cx={x} cy={yPx(entropyMax)} r="4.5" fill="none" stroke={accentBlue} strokeWidth="2" />
          <line x1={x} x2={x} y1={yPx(entropyMax)} y2={yPx(entropy)} stroke={coral} strokeWidth="2" strokeDasharray="4 3" />
          <circle cx={x} cy={yPx(entropy)} r="5.5" fill={coral} />
          {gap > 0.05 && (
            <text x={x + 9} y={(yPx(entropy) + yPx(entropyMax)) / 2 + 6} fill={coral} fontSize="16">
              Gap {gap.toFixed(2)} Bits
            </text>
          )}
        </>
      )}
    </svg>
  );
}

function RefTriangle() {
  const a = [65, 22];
  const b = [26, 82];
  const c = [104, 82];
  return (
    <svg viewBox="0 0 130 104" width="110" height="88" aria-hidden="true">
      {[
        [a, b],
        [a, c],
        [b, c],
      ].map(([start, end], index) => (
        <line
          key={index}
          x1={start[0]}
          y1={start[1]}
          x2={end[0]}
          y2={end[1]}
          stroke="var(--mx-border-secondary)"
          strokeWidth="1.5"
          strokeDasharray="3 3"
        />
      ))}
      {[a, b, c].map((point, index) => (
        <circle key={index} cx={point[0]} cy={point[1]} r="6" fill="var(--mx-text-primary)" />
      ))}
      <text x="65" y="12" textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="12">
        A
      </text>
      <text x="14" y="88" textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="12">
        B
      </text>
      <text x="116" y="88" textAnchor="middle" fill="var(--mx-text-secondary)" fontSize="12">
        C
      </text>
    </svg>
  );
}

function Metric({label, value, accent}: {label: React.ReactNode; value: string; accent?: string}) {
  return (
    <div className={styles.metric}>
      <div className={styles.metricLabel}>{label}</div>
      <div className={styles.metricValue} style={{color: accent ?? 'var(--mx-text-primary)'}}>
        {value}
      </div>
    </div>
  );
}

export default function MaxentGraphExample() {
  const [mode, setMode] = useState<Mode>('edge');
  const [meanTarget, setMeanTarget] = useState(1.5);
  const [degreeTargets, setDegreeTargets] = useState({A: 1, B: 1, C: 1});
  const [freeProbabilities, setFreeProbabilities] = useState(() => new Array(8).fill(1 / 8));

  const current = useMemo(() => {
    if (mode === 'edge') {
      const p = clamp(meanTarget / 3, 0, 1);
      return {probabilities: edgeProbsToP([p, p, p]), edgeProbabilities: [p, p, p], feasible: true};
    }
    if (mode === 'degree') {
      const {A, B, C} = degreeTargets;
      const raw = [(A + B - C) / 2, (A + C - B) / 2, (B + C - A) / 2];
      const edgeProbabilities = raw.map((value) => clamp(value, 0, 1));
      return {
        probabilities: edgeProbsToP(edgeProbabilities),
        edgeProbabilities,
        feasible: edgeProbabilities.every((value, index) => Math.abs(value - raw[index]) < 1e-9),
      };
    }
    return {probabilities: freeProbabilities, edgeProbabilities: null, feasible: true};
  }, [degreeTargets, freeProbabilities, meanTarget, mode]);

  const mean = meanEdges(current.probabilities);
  const entropy = entropyBits(current.probabilities);
  const entropyMax = maxEntropyBits(mean);
  const gap = entropyMax - entropy;

  const updateFreeProbability = (index: number, probability: number) => {
    setFreeProbabilities((previous) => {
      const next = [...previous];
      const target = clamp(probability, 0, 1);
      const others = previous.reduce((sum, value, currentIndex) => (currentIndex === index ? sum : sum + value), 0);
      const remaining = 1 - target;
      for (let i = 0; i < next.length; i += 1) {
        if (i === index) continue;
        next[i] = others > 1e-9 ? previous[i] * (remaining / others) : remaining / 7;
      }
      next[index] = target;
      const total = next.reduce((sum, value) => sum + value, 0);
      return next.map((value) => value / total);
    });
  };

  const chooseMode = (nextMode: Mode) => {
    if (nextMode === 'free' && mode !== 'free') {
      setFreeProbabilities(current.probabilities);
    }
    setMode(nextMode);
  };

  const probability = clamp(meanTarget / 3, 0, 1);
  const lambdaTex =
    probability <= 1e-6
      ? '+\\infty'
      : probability >= 1 - 1e-6
        ? '-\\infty'
        : Math.log((1 - probability) / probability).toFixed(2);
  const edgeProbabilities = current.edgeProbabilities ?? [0, 0, 0];
  const achievedDegrees = [
    edgeProbabilities[0] + edgeProbabilities[1],
    edgeProbabilities[0] + edgeProbabilities[2],
    edgeProbabilities[1] + edgeProbabilities[2],
  ];

  return (
    <div className={styles.figure}>
      <div className={styles.wrapper}>
        <h2 className={styles.srOnly}>
          Interactive maximum-entropy graph ensemble on three nodes. Choose a constraint on total edge count or on individual node degrees,
          or edit the distribution freely.
        </h2>

        <div className={styles.controlArea}>
          <div className={styles.modeTabs} role="tablist" aria-label="Constraint mode">
            {[
              ['edge', 'Constrain total edges'],
              ['degree', 'Constrain node degrees'],
              ['free', 'Free play'],
            ].map(([key, label]) => (
              <button
                key={key}
                className={`${styles.modeTab} ${mode === key ? styles.activeModeTab : ''}`}
                type="button"
                role="tab"
                aria-selected={mode === key}
                onClick={() => chooseMode(key as Mode)}
              >
                {label}
              </button>
            ))}
          </div>

          <div className={styles.controlPanel}>
            {mode === 'edge' && (
              <>
                <div className={styles.controlRow}>
                  <label className={styles.wideLabel} htmlFor="maxent-edge-target">
                    Target Expected Edges <InlineMath tex={'\\langle L\\rangle'} />
                  </label>
                  <input
                    id="maxent-edge-target"
                    type="range"
                    min="0"
                    max="3"
                    step="0.05"
                    value={meanTarget}
                    onChange={(event) => setMeanTarget(Number(event.target.value))}
                  />
                  <span className={styles.output}>{meanTarget.toFixed(2)}</span>
                </div>
                <div className={styles.hint}>
                  a single constraint shared by all three possible edges
                </div>
              </>
            )}

            {mode === 'degree' && (
              <>
                <div className={styles.degreeControls}>
                  <RefTriangle />
                  <div className={styles.degreeSliders}>
                    {(['A', 'B', 'C'] as const).map((node) => (
                      <div className={styles.degreeRow} key={node}>
                        <label htmlFor={`maxent-degree-${node}`}>
                          Node {node} &lt;k<sub>{node}</sub>&gt;
                        </label>
                        <input
                          id={`maxent-degree-${node}`}
                          type="range"
                          min="0.2"
                          max="1.8"
                          step="0.05"
                          value={degreeTargets[node]}
                          onChange={(event) => setDegreeTargets((previous) => ({...previous, [node]: Number(event.target.value)}))}
                        />
                        <span className={styles.output}>{degreeTargets[node].toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className={styles.hint}>one constraint per node, which induces one probability per possible edge</div>
              </>
            )}

            {mode === 'free' && (
              <div className={styles.freeControls}>
                <span>drag any bar up or down to reshape P(G)</span>
                <button
                  type="button"
                  onClick={() => {
                    const p = clamp(meanEdges(freeProbabilities) / 3, 0, 1);
                    setFreeProbabilities(edgeProbsToP([p, p, p]));
                  }}
                >
                  Snap to max-entropy
                </button>
                <button type="button" onClick={() => setFreeProbabilities(new Array(8).fill(1 / 8))}>
                  Uniform
                </button>
              </div>
            )}
          </div>

          <div className={styles.formula}>
            {mode === 'edge' && (
              <>
                <p>
                  <InlineMath tex={`p=\\langle L\\rangle/3=${probability.toFixed(2)}`} />;{' '}
                  <InlineMath tex={`\\lambda=\\log\\frac{1-p}{p}=${lambdaTex}`} />
                </p>
              </>
            )}
            {mode === 'degree' && (
              <>
                <p>
                  <InlineMath
                    tex={`p_{AB}=\\frac{k_A+k_B-k_C}{2}=${edgeProbabilities[0].toFixed(2)}`}
                  />
                  , <InlineMath tex={`p_{AC}=${edgeProbabilities[1].toFixed(2)}`} />,{' '}
                  <InlineMath tex={`p_{BC}=${edgeProbabilities[2].toFixed(2)}`} />
                </p>
                <p className={styles.muted}>
                  Achieved degrees:{' '}
                  <InlineMath
                    tex={`k_A=${achievedDegrees[0].toFixed(2)},\\ k_B=${achievedDegrees[1].toFixed(2)},\\ k_C=${achievedDegrees[2].toFixed(2)}`}
                  />
                </p>
                {!current.feasible && (
                  <p className={styles.warning}>
                    These targets are not jointly realizable on three nodes, so the edge probabilities were clamped to [0,1] and the achieved
                    degrees differ from the targets.
                  </p>
                )}
              </>
            )}
            {mode === 'free' && (
              <p>
                Drag the bars to make any normalized <InlineMath tex="P(G)" /> and compare it with the maximum-entropy ceiling at the same{' '}
                <InlineMath tex={'\\langle L\\rangle'} />.
              </p>
            )}
          </div>
        </div>

        <div className={styles.chartTitle}>Graph Probability Distribution P(G)</div>
        <ProbabilityMassChart probabilities={current.probabilities} mode={mode} onFreeProbabilityChange={updateFreeProbability} />

        <div className={styles.chartRow}>
          <div className={styles.chartPanel}>
              <div className={styles.chartTitleRow}>
                <div className={styles.chartTitle}>Edge Count Distribution P(L)</div>
              <div className={styles.meanBadge}>
                <InlineMath tex={`\\langle L\\rangle=${mean.toFixed(2)}`} />
              </div>
            </div>
            <EdgeCountChart probabilities={current.probabilities} mean={mean} />
          </div>
          <div className={styles.chartPanel}>
            <div className={styles.chartTitle}>Entropy Versus Expected Edge Count</div>
            <EntropyChart mean={mean} entropy={entropy} entropyMax={entropyMax} />
          </div>
        </div>

        <div className={styles.metrics}>
          <Metric
            label={
              <>
                Expected Edges <InlineMath tex={'\\langle L\\rangle'} />
              </>
            }
            value={mean.toFixed(2)}
          />
          <Metric label="Entropy" value={`${entropy.toFixed(2)} Bits`} />
          <Metric
            label={
              <>
                Max At This <InlineMath tex={'\\langle L\\rangle'} />
              </>
            }
            value={`${entropyMax.toFixed(2)} Bits`}
          />
          <Metric label="Entropy Gap" value={`${gap.toFixed(2)} Bits`} accent={gap < 0.012 ? undefined : coral} />
        </div>
      </div>

      <div className={styles.legend}>
        <span>
          <span className={styles.swatch} style={{background: accentBlue}} />
          Blue: The Maximum (Ceiling)
        </span>
        <span>
          <span className={styles.swatch} style={{background: coral}} />
          Coral: The Gap (What Structure Costs)
        </span>
      </div>
    </div>
  );
}
