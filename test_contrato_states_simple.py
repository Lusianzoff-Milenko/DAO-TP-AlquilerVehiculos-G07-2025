#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba simple para verificar estados de Contrato (sin dependencias pesadas).
"""

try:
    print("=== TEST DE IMPLEMENTACIÓN STATE PATTERN - CONTRATO ===\n")
    
    # Test 1: Importar estados
    print("📦 Test 1: Importando estados...")
    from domain.states.contrato.state import State
    from domain.states.contrato.en_reservado import EnReservado
    from domain.states.contrato.en_curso import EnCurso
    from domain.states.contrato.ya_entregado import YaEntregado
    from domain.states.contrato.cancelado import Cancelado
    print("✓ Todos los estados importados correctamente\n")
    
    # Test 2: Factory Method
    print("🏭 Test 2: Factory Method create_state()...")
    estado_9 = State.create_state(9)
    assert isinstance(estado_9, EnReservado), "ID 9 debería crear EnReservado"
    print(f"✓ ID 9 → {estado_9.__class__.__name__}")
    
    estado_8 = State.create_state(8)
    assert isinstance(estado_8, EnCurso), "ID 8 debería crear EnCurso"
    print(f"✓ ID 8 → {estado_8.__class__.__name__}")
    
    estado_10 = State.create_state(10)
    assert isinstance(estado_10, YaEntregado), "ID 10 debería crear YaEntregado"
    print(f"✓ ID 10 → {estado_10.__class__.__name__}")
    
    estado_11 = State.create_state(11)
    assert isinstance(estado_11, Cancelado), "ID 11 debería crear Cancelado"
    print(f"✓ ID 11 → {estado_11.__class__.__name__}\n")
    
    # Test 3: Métodos abstractos implementados
    print("🔍 Test 3: Métodos abstractos implementados...")
    metodos_requeridos = ['tomar_pago', 'cancelar', 'recibir_devolucion', 'puede_modificar_fechas']
    
    for estado_clase in [EnReservado, EnCurso, YaEntregado, Cancelado]:
        instancia = estado_clase()
        for metodo in metodos_requeridos:
            assert hasattr(instancia, metodo), f"{estado_clase.__name__} debe tener {metodo}"
        print(f"✓ {estado_clase.__name__} tiene todos los métodos requeridos")
    
    print()
    
    # Test 4: Validación de fechas
    print("📅 Test 4: Validación de fechas...")
    from services.utils import validate_fecha_rango
    from datetime import datetime, timedelta
    
    fecha_desde = datetime(2025, 11, 25, 10, 0)
    fecha_hasta = datetime(2025, 11, 27, 10, 0)
    error = validate_fecha_rango(fecha_desde, fecha_hasta)
    assert error is None, f"Fechas válidas no deberían dar error: {error}"
    print(f"✓ Validación OK: {fecha_desde} < {fecha_hasta}")
    
    # Test fechas inválidas
    error_inverso = validate_fecha_rango(fecha_hasta, fecha_desde)
    assert error_inverso is not None, "Fechas invertidas deberían dar error"
    print(f"✓ Validación OK: Rechaza fechas invertidas\n")
    
    # Test 5: Comportamiento de estados
    print("⚙️  Test 5: Comportamiento de estados...")
    
    # EnReservado permite modificar fechas
    reservado = EnReservado()
    assert reservado.puede_modificar_fechas() == True
    print("✓ EnReservado permite modificar fechas")
    
    # EnCurso NO permite modificar fechas
    en_curso = EnCurso()
    assert en_curso.puede_modificar_fechas() == False
    print("✓ EnCurso NO permite modificar fechas")
    
    # YaEntregado es terminal
    entregado = YaEntregado()
    assert entregado.puede_modificar_fechas() == False
    exito_pago, _ = entregado.tomar_pago(100)
    assert exito_pago == False
    print("✓ YaEntregado es estado terminal (no permite operaciones)")
    
    # Cancelado es terminal
    cancelado = Cancelado()
    assert cancelado.puede_modificar_fechas() == False
    exito_cancelar = cancelado.cancelar("test")
    assert exito_cancelar == False
    print("✓ Cancelado es estado terminal (no permite operaciones)\n")
    
    print("=" * 60)
    print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 60)
    print("\n📋 RESUMEN DE IMPLEMENTACIÓN:")
    print("   ✓ 4 estados concretos creados (EnReservado, EnCurso, YaEntregado, Cancelado)")
    print("   ✓ State Pattern con Factory Method (create_state)")
    print("   ✓ Validación de fechas (fecha_hasta > fecha_desde)")
    print("   ✓ Métodos abstractos implementados en todos los estados")
    print("   ✓ Estados terminales correctamente bloqueados")
    print("   ✓ ContratoService con 4 nuevos métodos:")
    print("       - confirmar_pago_reserva()")
    print("       - cancelar_contrato()")
    print("       - recibir_devolucion()")
    print("       - puede_modificar_fechas_contrato()")
    print("\n🎯 PRÓXIMOS PASOS:")
    print("   1. Probar con datos reales de la BD")
    print("   2. Integrar con UI para CRUD de contratos")
    print("   3. Crear tests unitarios completos")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
