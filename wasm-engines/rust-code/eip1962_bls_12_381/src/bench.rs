use eip1962::engines::bls12_381::*;
use eip1962::weierstrass::curve::{CurvePoint};
use eip1962::weierstrass::{CurveOverFpParameters, CurveOverFp2Parameters};
use eip1962::traits::{ZeroAndOne};
use eip1962::extension_towers::fp12_as_2_over3_over_2::{Fp12};
use eip1962::extension_towers::fp2::Fp2;
use eip1962::field::{U384Repr, PrimeField};
use eip1962::fp::Fp;
use eip1962::{decl_fp, decl_fp2};

const SIZE_F1: usize = 6;
const SIZE_P_G1: usize = SIZE_F1 * 3;
const SIZE_P_G2: usize = SIZE_F1 * 6;
const INPUT_SIZE: usize = SIZE_P_G1 + SIZE_P_G2;

fn parse_g1_point(data: &[u8]) -> CurvePoint<CurveOverFpParameters<'static, U384Repr, PrimeField<U384Repr>>> {
    let p_x = Fp::from_be_bytes(&BLS12_381_FIELD, &data[0..48], true).expect("invalid point");
    let p_y = Fp::from_be_bytes(&BLS12_381_FIELD, &data[48..96], true).expect("invalid point");

    println!("fuck {:?}", p_x);
    CurvePoint::point_from_xy(&BLS12_381_G1_CURVE, p_x, p_y)
}

fn parse_g2_point(data: &[u8]) -> CurvePoint<CurveOverFp2Parameters<'static, U384Repr, PrimeField<U384Repr>>> {
    let p_x_0 = Fp::from_be_bytes(&BLS12_381_FIELD, &data[0..48], true).expect("invalid point");
    let p_x_1 = Fp::from_be_bytes(&BLS12_381_FIELD, &data[48..96], true).expect("invalid point");
    let p_y_0 = Fp::from_be_bytes(&BLS12_381_FIELD, &data[96..144], true).expect("invalid point");
    let p_y_1 = Fp::from_be_bytes(&BLS12_381_FIELD, &data[144..192], true).expect("invalid point");

    let mut p_x = Fp2::zero(&BLS12_381_EXTENSION_2_FIELD);
    let mut p_y = Fp2::zero(&BLS12_381_EXTENSION_2_FIELD);

    p_x.c0 = p_x_0;
    p_x.c1 = p_x_1;
    p_y.c0 = p_y_0;
    p_y.c1 = p_y_1;

    CurvePoint::point_from_xy(&BLS12_381_G2_CURVE, p_x, p_y)
}

pub fn bench(input: &[u8]) {
    let p1 = parse_g1_point(input);
    let p2 = parse_g2_point(&input[96..192]);
}

#[cfg(test)]
mod tests {
    use eip1962::engines::bls12_381::*;
    use eip1962::weierstrass::curve::{CurvePoint};
    use eip1962::weierstrass::{CurveOverFpParameters, CurveOverFp2Parameters};
    use eip1962::traits::{ZeroAndOne};
    use eip1962::extension_towers::fp12_as_2_over3_over_2::{Fp12};
    use eip1962::extension_towers::fp2::Fp2;
    use eip1962::field::{U384Repr, PrimeField};
    use eip1962::fp::Fp;
    use eip1962::{decl_fp, decl_fp2};
    use super::{parse_g2_point, parse_g1_point};

    #[test]
    pub fn test_g1_g2_parse() {
        let g1_bytes = [23u8,241u8,211u8,167u8,49u8,151u8,215u8,148u8,38u8,149u8,99u8,140u8,79u8,169u8,172u8,15u8,195u8,104u8,140u8,79u8,151u8,116u8,185u8,5u8,161u8,78u8,58u8,63u8,23u8,27u8,172u8,88u8,108u8,85u8,232u8,63u8,249u8,122u8,26u8,239u8,251u8,58u8,240u8,10u8,219u8,34u8,198u8,187u8,8u8,179u8,244u8,129u8,227u8,170u8,160u8,241u8,160u8,158u8,48u8,237u8,116u8,29u8,138u8,228u8,252u8,245u8,224u8,149u8,213u8,208u8,10u8,246u8,0u8,219u8,24u8,203u8,44u8,4u8,179u8,237u8,208u8,60u8,199u8,68u8,162u8,136u8,138u8,228u8,12u8,170u8,35u8,41u8,70u8,197u8,231u8,225u8]; 

        let p1 = parse_g1_point(&g1_bytes[0..96]);

        assert!(p1.x == BLS12_381_G1_GENERATOR.x);
        assert!(p1.y == BLS12_381_G1_GENERATOR.y);
        assert!(p1.z == BLS12_381_G1_GENERATOR.z);

        println!("x = {}", &BLS12_381_G2_GENERATOR.x);
        println!("y = {}", &BLS12_381_G2_GENERATOR.y);
        println!("z = {}", &BLS12_381_G2_GENERATOR.z);

        let g2_bytes = [2u8,74u8,162u8,178u8,240u8,143u8,10u8,145u8,38u8,8u8,5u8,39u8,45u8,197u8,16u8,81u8,198u8,228u8,122u8,212u8,250u8,64u8,59u8,2u8,180u8,81u8,11u8,100u8,122u8,227u8,209u8,119u8,11u8,172u8,3u8,38u8,168u8,5u8,187u8,239u8,212u8,128u8,86u8,200u8,193u8,33u8,189u8,184u8,19u8,224u8,43u8,96u8,82u8,113u8,159u8,96u8,125u8,172u8,211u8,160u8,136u8,39u8,79u8,101u8,89u8,107u8,208u8,208u8,153u8,32u8,182u8,26u8,181u8,218u8,97u8,187u8,220u8,127u8,80u8,73u8,51u8,76u8,241u8,18u8,19u8,148u8,93u8,87u8,229u8,172u8,125u8,5u8,93u8,4u8,43u8,126u8,12u8,229u8,213u8,39u8,114u8,125u8,110u8,17u8,140u8,201u8,205u8,198u8,218u8,46u8,53u8,26u8,173u8,253u8,155u8,170u8,140u8,189u8,211u8,167u8,109u8,66u8,154u8,105u8,81u8,96u8,209u8,44u8,146u8,58u8,201u8,204u8,59u8,172u8,162u8,137u8,225u8,147u8,84u8,134u8,8u8,184u8,40u8,1u8,6u8,6u8,196u8,160u8,46u8,167u8,52u8,204u8,50u8,172u8,210u8,176u8,43u8,194u8,139u8,153u8,203u8,62u8,40u8,126u8,133u8,167u8,99u8,175u8,38u8,116u8,146u8,171u8,87u8,46u8,153u8,171u8,63u8,55u8,13u8,39u8,92u8,236u8,29u8,161u8,170u8,169u8,7u8,95u8,240u8,95u8,121u8,190u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,1u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8,0u8];

        let p2 = parse_g2_point(&g2_bytes[0..288]);

        assert!(&p2.x.c0 == &BLS12_381_G2_GENERATOR.x.c0, format!("{} != {}", &p2.x.c0, &BLS12_381_G2_GENERATOR.x.c0));
        assert!(&p2.x.c1 == &BLS12_381_G2_GENERATOR.x.c1, format!("{} != {}", &p2.x.c0, &BLS12_381_G2_GENERATOR.x.c0));

        assert!(&p2.y.c0 == &BLS12_381_G2_GENERATOR.y.c0, format!("{} != {}", &p2.x.c0, &BLS12_381_G2_GENERATOR.x.c0));
        assert!(&p2.y.c1 == &BLS12_381_G2_GENERATOR.y.c1, format!("{} != {}", &p2.x.c0, &BLS12_381_G2_GENERATOR.x.c0));

        assert!(&p2.z.c0 == &BLS12_381_G2_GENERATOR.z.c0, format!("{} != {}", &p2.x.c0, &BLS12_381_G2_GENERATOR.x.c0));
        assert!(&p2.z.c1 == &BLS12_381_G2_GENERATOR.z.c1, format!("{} != {}", &p2.x.c0, &BLS12_381_G2_GENERATOR.x.c0));
    }
}
