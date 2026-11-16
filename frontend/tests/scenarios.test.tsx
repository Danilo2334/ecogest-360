import {render,screen,cleanup,fireEvent,waitFor} from '@testing-library/react';
import {it,expect,vi,afterEach} from 'vitest';
import {ScenarioPage} from '../src/features/scenarios/ScenarioPage';
import {api} from '../src/services/api';
vi.mock('../src/services/api',()=>({api:vi.fn()}));
afterEach(()=>{cleanup();vi.resetAllMocks()});
const base={generated:'25',verified_compost:'20',pending:'5',rate:'80'};
it('envía hipótesis y token, distingue base de resultado sin escritura ambiental',async()=>{
 const response={base:{...base,provenance:'simulado',cutoff:'2026-11-15T12:00:00Z'},result:base,eligible:'5',nonrecoverable:'0',base_token:'token',filters:{provenance:'simulado'},formula:'A+x',limitations:'Hipótesis',delta:{generated:'0',verified_compost:'0',generated_percent:'0',rate_points:'0'},amount:'0'};
 vi.mocked(api).mockResolvedValue(response);
 render(<ScenarioPage query="provenance=simulado"/>);
 expect(await screen.findByText('Límite de esta base: 5 kg')).toBeVisible();
 fireEvent.change(screen.getByLabelText('Cantidad hipotética (kg)'),{target:{value:'3'}});
 fireEvent.click(screen.getByRole('button',{name:'Calcular escenario'}));
 await waitFor(()=>expect(api).toHaveBeenLastCalledWith('v2/scenarios/preview',expect.objectContaining({amount:'3',base_token:'token'})));
 expect(screen.getByText('No modifica mediciones ni datos operativos.')).toBeVisible();
});
