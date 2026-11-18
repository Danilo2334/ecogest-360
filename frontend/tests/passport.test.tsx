import {render,screen,cleanup,fireEvent} from '@testing-library/react';
import {it,expect,vi,afterEach} from 'vitest';
import {PassportPage} from '../src/features/lots/PassportPage';
import {api} from '../src/services/api';
vi.mock('../src/services/api',()=>({api:vi.fn()}));
afterEach(()=>{cleanup();vi.resetAllMocks()});
it('muestra ausencia de autor y conserva salida compartida independiente',async()=>{
 vi.mocked(api).mockResolvedValue({lot:{id:1,public_id:'uuid',provenance:'simulado',state:'abierto'},balance:{assigned:'25',available:'15',consumed:'10'},sources:[],events:[{key:'1',kind:'lote',date:'2026-11-15T12:00:00Z',actor:null,kg:'25',balance_effect:'25',description:'Creación'}],processes:[{id:1,state:'finalizado',provenance:'simulado',lot_input:'10',total_input:'20',output:'8',shared:true,verified:false}],cutoff:'2026-11-15T13:00:00Z',limitations:'No es certificado'});
 render(<PassportPage uuid="uuid" onBack={()=>{}}/>);
 expect(await screen.findByText(/Proceso compartido/)).toBeInTheDocument();
 fireEvent.click(screen.getByText('Ver responsable y evidencia'));
 expect(screen.getByText(/No disponible en el registro original/)).toBeVisible();
 expect(screen.getByText(/Salida independiente: 8 kg/)).toBeVisible();
});
it('no inventa contenido cuando el servidor deniega la consulta',async()=>{
 vi.mocked(api).mockRejectedValue(new Error('No disponible'));
 render(<PassportPage uuid="ajeno" onBack={()=>{}}/>);
 expect(await screen.findByRole('alert')).toHaveTextContent('No disponible');
 expect(screen.queryByText(/La historia del lote/)).not.toBeInTheDocument();
});
